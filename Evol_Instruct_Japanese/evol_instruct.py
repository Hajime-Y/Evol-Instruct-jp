import random
from tqdm.auto import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

from mixtral_access import call_chatmodel, compare_evol_instructions, check_hallucination
from depth import createConstraintsPrompt, createDeepenPrompt, createConcretizingPrompt, createReasoningPrompt
from breadth import createBreadthPrompt
from eliminte import createEliminateComparePrompt, createEliminateHallucinationPrompt, check_difficulty, check_punctuation_stopwords, check_copied_words


def evol_instruct(all_objs, model="mistralai/Mixtral-8x22B-Instruct-v0.1", hallucination_check_model="mistralai/Mixtral-8x7B-Instruct-v0.1", stop_words=[], final_gen_flg=False):
	"""
    渡されたInstructionを含む辞書リスト(all_objs)に対して、evol_instructを行う。
	成功したinstructionを含む辞書リスト(evol_objs)と失敗したinstructionを含む辞書リスト(pool_objs)を返す。

    Args:
        all_objs (list): 進化させる指示のリスト。
        model (str): 使用するモデルの名前。デフォルトは 'mistralai/Mixtral-8x22B-Instruct-v0.1'。
        hallucination_check_model (str): 存在しない単語・概念等が含まれるかどうかを確認するモデルの名前。modelとは異なるモデルを指定することを推奨。デフォルトは 'mistralai/Mixtral-8x7B-Instruct-v0.1'。
        stop_words (list): ストップワードのリスト。デフォルトは空のリスト。
		final_gen_flg (bool): 最終世代(Answerが必要な世代)かどうかのフラグ。デフォルトはFalse。

    Returns:
        tuple: 成功したinstructionを含む辞書リスト(evol_objs),失敗したinstructionを含む辞書リスト(pool_objs),現在の世代(generation)のタプル。
    """

	evol_objs = []  # 保存用リスト
	pool_objs = []  # 失敗したInstructionの退避用リスト
    
    # 進化させるリストがない時
	if not all_objs:
		return evol_objs, pool_objs
	
	with ThreadPoolExecutor() as executor:
		futures = [executor.submit(process_obj, obj, model, hallucination_check_model, stop_words, final_gen_flg) for obj in all_objs]
		for future in as_completed(futures):
			category, result = future.result()
			if category == "eliminated":
				pool_objs.append(result)
			else:
				evol_objs.append(result)
				
	# all_objsのIDの順番に直す
	evol_objs = sorted(evol_objs, key=lambda x: all_objs.index(next(obj for obj in all_objs if obj["id"] == x["id"])))
	pool_objs = sorted(pool_objs, key=lambda x: all_objs.index(next(obj for obj in all_objs if obj["id"] == x["id"])))
	
	return evol_objs, pool_objs


def process_obj(cur_obj, model, hallucination_check_model, stop_words, answer_flg):
	# ID
    origin_id = cur_obj.get("id", "")
    # 世代
    generation = cur_obj.get("generation", 0) + 1
    # 進化の歴史
    evol_history = cur_obj.get("evol_history", [])
    
    # 幅進化の倍率(:breadth_mult)：Instructionが複雑になる前の方が幅進化が上手く行きやすい気がする
    breadth_mult = calculate_breadth_multiplier(evol_history)

    # 初期Instruction
    if cur_obj.get("input"):
        instruction = cur_obj['instruction'].strip() + '\n'+ cur_obj['input'].strip()
    else:
        instruction = cur_obj['instruction'].strip()

    # 進化方法の選定(prompt, evol_type)
    selected_evol_prompt, selected_evol_type = select_evolution_prompt(instruction, breadth_mult)
    evol_history += [selected_evol_type]  # 進化の歴史の更新

    # Instructionの進化
    evol_instruction = call_chatmodel(selected_evol_prompt, model_name=model)

    # "Translation:"以下の削除（Mixtralを使った場合、たまに入る）
    if "Translation:" in evol_instruction:
        evol_instruction = evol_instruction.split("Translation:")[0].strip()

    # 進化したInstructionのチェック
    # 1. instruction, evol_instructionが同等かどうか
    check_prompt = createEliminateComparePrompt(instruction, evol_instruction)
    if compare_evol_instructions(check_prompt, model_name=model):
        return "eliminated", {"id": origin_id, "generation": generation, "evol_history": evol_history, "instruction": evol_instruction, "output": "", "type": 1}

    # 4. 進化した命令が進化するプロンプトからいくつかの単語を明らかにコピーしているかどうか
    if check_copied_words(evol_instruction):
        return "eliminated", {"id": origin_id, "generation": generation, "evol_history": evol_history, "instruction": evol_instruction, "output": "", "type": 4}
    
    # 5. instructionに存在しない単語・概念等が含まれるかどうか（追加）
    check_prompt = createEliminateHallucinationPrompt(evol_instruction)
    if not check_hallucination(check_prompt, model_name=hallucination_check_model):
        return "eliminated", {"id": origin_id, "generation": generation, "evol_history": evol_history, "instruction": evol_instruction, "output": "", "type": 5}
    
    # 回答の生成
    if answer_flg:
        answer = call_chatmodel(evol_instruction+"\nYou must point out any uncertainties or misunderstandings in the instruction and provide as factual a response as possible.\nAnswer in Japanese, not in English.", model_name=model)
    else:
        # 回答の生成を行わない場合、この時点でInstructionの進化成功として返す
        return "evolved", {"id": origin_id, "generation": generation, "evol_history": evol_history, "instruction":evol_instruction, "output":""}
    
    # 回答のチェック(機械的)
    # 2. 進化した命令がLLMにとって応答を生成することが困難かどうか
    # 3. LLMが生成した応答が句読点とストップワードのみを含むかどうか
    if check_difficulty(answer):
        return "eliminated", {"id": origin_id, "generation": generation, "evol_history": evol_history, "instruction": evol_instruction, "output": answer, "type": 2}
    elif check_punctuation_stopwords(answer, stop_words):
        return "eliminated", {"id": origin_id, "generation": generation, "evol_history": evol_history, "instruction": evol_instruction, "output": answer, "type": 3}
    else:
        return "evolved", {"id": origin_id, "generation": generation, "evol_history": evol_history, "instruction":evol_instruction, "output":answer}


def calculate_breadth_multiplier(evol_history):
    """
    evol_historyリストからbreadthの出現回数に基づいてbreadth_multを計算する。

    Args:
        evol_history (list): 進化の歴史を記録したリスト。

    Returns:
        int: 幅進化の倍率。
    """
    breadth_count = evol_history.count("breadth")
    if breadth_count == 0:
        return 4
    elif breadth_count == 1:
        return 3
    else:
        return 1
	

def select_evolution_prompt(instruction, breadth_mult):
    """
    指定されたinstructionとbreadth_multに基づいて、進化方法を選定し、選ばれたpromptとevol_typeを返す。

    Args:
        instruction (str): 進化させるための元の指示文。
        breadth_mult (int): breadthの確率を上げる倍率。

    Returns:
        tuple: 選ばれたpromptとevol_typeのタプル。
    """
    evol_prompts = []
    evol_prompts.append({"prompt": createConstraintsPrompt(instruction), "evol_type": "constraints"})
    evol_prompts.append({"prompt": createDeepenPrompt(instruction), "evol_type": "deepen"})
    evol_prompts.append({"prompt": createConcretizingPrompt(instruction), "evol_type": "concretizing"})
    evol_prompts.append({"prompt": createReasoningPrompt(instruction), "evol_type": "reasoning"})
    for _ in range(breadth_mult):
        evol_prompts.append({"prompt": createBreadthPrompt(instruction), "evol_type": "breadth"})

    selected = random.choice(evol_prompts)
    return selected["prompt"], selected["evol_type"]