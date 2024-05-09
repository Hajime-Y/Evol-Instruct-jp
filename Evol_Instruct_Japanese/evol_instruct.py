import random
from tqdm.auto import tqdm

from mixtral_access import call_chatmodel, check_evol_instruction
from depth import createConstraintsPrompt, createDeepenPrompt, createConcretizingPrompt, createReasoningPrompt
from breadth import createBreadthPrompt
from eliminte import createEliminatePrompt, check_difficulty, check_punctuation_stopwords, check_copied_words


def evol_instruct(all_objs, model="mistralai/Mixtral-8x22B-Instruct-v0.1", stop_words=[]):
	"""
    渡されたInstructionを含む辞書リスト(all_objs)に対して、evol_instructを行う。
	成功したinstructionを含む辞書リスト(evol_objs)と失敗したinstructionを含む辞書リスト(pool_objs)を返す。

    Args:
        all_objs (list): 進化させる指示のリスト。
        model (str): 使用するモデルの名前。デフォルトは 'mistralai/Mixtral-8x22B-Instruct-v0.1'。
        stop_words (list): ストップワードのリスト。デフォルトは空のリスト。

    Returns:
        tuple: 成功したinstructionを含む辞書リスト(evol_objs),失敗したinstructionを含む辞書リスト(pool_objs),現在の世代(generation)のタプル。
    """

	evol_objs = []  # 保存用リスト
	pool_objs = []  # 失敗したInstructionの退避用リスト
	for cur_obj in tqdm(all_objs):
		# ID
		origin_id = cur_obj.get("id", "")
		# 世代
		generation = cur_obj.get("generation", 0) + 1
		# 進化の歴史
		evol_history = cur_obj.get("evol_history", [])

		# 初期Instruction
		if 'instances' in cur_obj and 'input' in cur_obj["instances"][0]:
			instruction = cur_obj['instruction'].strip() + '\n'+ cur_obj["instances"][0]['input'].strip()
		else:
			instruction = cur_obj['instruction'].strip()

		# 進化方法の選定(prompt, evol_type)
		evol_prompts = []
		evol_prompts.append({"prompt": createConstraintsPrompt(instruction), "evol_type": "constraints"})
		evol_prompts.append({"prompt": createDeepenPrompt(instruction), "evol_type": "deepen"})
		evol_prompts.append({"prompt": createConcretizingPrompt(instruction), "evol_type": "concretizing"})
		evol_prompts.append({"prompt": createReasoningPrompt(instruction), "evol_type": "reasoning"})
		# breadthの確立を上げる(他の2倍)
		for _ in range(2):
			evol_prompts.append({"prompt": createBreadthPrompt(instruction), "evol_type": "breadth"})

		selected = random.choice(evol_prompts)
		selected_evol_prompt = selected["prompt"]
		evol_history += [selected["evol_type"]]  # 進化の歴史の更新

		# Instructionの進化
		evol_instruction = call_chatmodel(selected_evol_prompt, model_name=model)

		# 進化したInstructionのチェック
		# 1. instruction, evol_instructionが同等かどうか
		check_prompt = createEliminatePrompt(instruction, evol_instruction)
		if check_evol_instruction(check_prompt, model_name=model):
			pool_objs.append({"id": origin_id, "generation": generation, "evol_history": evol_history, "instruction": evol_instruction, "output": "", "type": 1})
			continue

		# 4. 進化した命令が進化するプロンプトからいくつかの単語を明らかにコピーしているかどうか
		if check_copied_words(evol_instruction):
			pool_objs.append({"id": origin_id, "generation": generation, "evol_history": evol_history, "instruction": evol_instruction, "output": "", "type": 4})
			continue
		
		# 回答の生成
		answer = call_chatmodel(evol_instruction+"\nAnswer in Japanese, not in English.", model_name=model)
		
		# 回答のチェック(機械的)
		# 2. 進化した命令がLLMにとって応答を生成することが困難かどうか
		# 3. LLMが生成した応答が句読点とストップワードのみを含むかどうか
		if check_difficulty(answer):
			pool_objs.append({"id": origin_id, "generation": generation, "evol_history": evol_history, "instruction": evol_instruction, "output": answer, "type": 2})
		elif check_punctuation_stopwords(answer, stop_words):
			pool_objs.append({"id": origin_id, "generation": generation, "evol_history": evol_history, "instruction": evol_instruction, "output": answer, "type": 3})
		else:
			evol_objs.append({"id": origin_id, "generation": generation, "evol_history": evol_history, "instruction":evol_instruction, "output":answer})
	
	return evol_objs, pool_objs, generation