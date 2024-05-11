"""
main.py

run:
python main.py \
	--input_file "./data/alpaca_seed_tasks_jp.jsonl" \
	--output_file "./output/new_generation.json" \
	--eliminated_file "./output/eliminated.json" \
	--model "mistralai/Mixtral-8x22B-Instruct-v0.1" \
	--generations 3 \
	--num_instructions_to_generate 10 \
	--subset_size 10
"""

import os
import json
import copy
import argparse
from tqdm.auto import tqdm

from evol_instruct import evol_instruct
import utils

def parse_arguments():
	"""引数を設定"""
	parser = argparse.ArgumentParser(description='Process some integers.')
	parser.add_argument('--input_file', type=str, default='./data/seed_tasks_jp_cleaned.jsonl', help='Input file path')
	parser.add_argument('--output_file', type=str, default='./output/new_generation.json', help='Output file path for new generations')
	parser.add_argument('--eliminated_file', type=str, default='./output/eliminated.json', help='Output file path for eliminated items')
	parser.add_argument('--model', type=str, default='mistralai/Mixtral-8x22B-Instruct-v0.1', help='model name')
	parser.add_argument('--generations', type=int, default=3, help='Number of generations to evolve')
	parser.add_argument('--num_instructions_to_generate', type=int, default=10, help='Number of instructions to generate in final generation')
	parser.add_argument('--subset_size', type=int, default=-1, help='Specify the subset size of the dataset for evolution. Default is -1, which uses the entire dataset.')
	return parser.parse_args()



def main():
	args = parse_arguments()
	# ストップワードを定義
	stop_words = []
	# ファイルの詳細を取得
	input_file = args.input_file
	# 利用モデル
	model = args.model


	# ファイルを開く
	with open(input_file, 'r') as fr:
		all_objs = []
		if input_file.endswith('.json'):
			all_objs = json.load(fr)
		elif input_file.endswith('.jsonl'):
			for line in fr:
				try:
					obj = json.loads(line)
					all_objs.append(obj)
				except json.JSONDecodeError as e:
					print(f"Error on line {fr.line_num}: {line}")
					print(f"Error message: {e.msg}")
					raise


	# 現在の世代
	cur_gen = all_objs[0].get("generation", 0)

	# 最終世代
	final_gen = cur_gen + args.generations


	# 保存用辞書(全世代)の初期化
	all_evol_objs = utils.init_generation_keys(args.output_file, cur_gen, final_gen)
	# 失敗したInstructionの保存用辞書(全世代)の初期化
	all_pool_objs = utils.init_generation_keys(args.eliminated_file, cur_gen, final_gen)

	# 初期世代のオブジェクトを追加または更新（項目が重複する場合、重複しない項目のみ追加）（重複は、辞書を一度文字列に直して比較）
	if "gen_0" in all_evol_objs:
		existing_origins = {json.dumps(obj) for obj in all_evol_objs["gen_0"]}
		new_origins = [obj for obj in all_objs if json.dumps(obj) not in existing_origins]
		all_evol_objs["gen_0"].extend(new_origins)
	else:
		all_evol_objs["gen_0"] = all_objs

	# 初期データ数の確認
	first_count = len(all_evol_objs[f"gen_{final_gen}"])
	print("開始：保存ファイルに既に{}件のInstructionがあります。".format(first_count))
	print("　　　{}件を目標に生成を開始し、超えた場合自動でInstructionの生成を停止します。".format(args.num_instructions_to_generate))
	print("　　　進化世代数は {} 世代に設定されています。".format(args.generations))


	# 進捗バーの初期化
	pbar = tqdm(total=args.num_instructions_to_generate, initial=first_count, desc=f"Evolution Progress")
	

	# 複数回Instruction進化をnum_instructions_to_generate数に達するまで実施
	# ループ前の件数
	cur_count = len(all_evol_objs[f"gen_{final_gen}"])
	while cur_count < args.num_instructions_to_generate:
		next_all_objs = copy.deepcopy(all_objs)

		# サブセットサイズが設定されている場合、データセットを分割
		if args.subset_size > 0:
			subset_indices = range(0, len(next_all_objs), args.subset_size)
			subsets = [next_all_objs[i:i + args.subset_size] for i in subset_indices]
		else:
			subsets = [next_all_objs]  # サブセットなしで全データを使用

		for subset in tqdm(subsets, disable=len(subsets) == 1, desc="Subset Progress"):
			# 指定された世代までInstruction進化
			for gen_number in tqdm(range(cur_gen+1, final_gen+1), desc=f"Generation Progress"):
				# Instructionの進化
				evol_objs, pool_objs = evol_instruct(
					subset, 
					model=model, 
					stop_words=stop_words,
					final_gen_flg=(gen_number==final_gen),  # 最終世代のみAnswerを生成
				)
				# 格納
				all_evol_objs[f"gen_{gen_number}"].extend(copy.deepcopy(evol_objs))  # 辞書の操作は参照によるもの。evol_objsの変更がall_evol_ojsに影響を与えないようにdeepcopyする。
				all_pool_objs[f"gen_{gen_number}"].extend(copy.deepcopy(pool_objs))  # 同上

				# 次の世代の元を入れ替え
				subset = evol_objs

			# 結果途中出力
			utils.update_json_file(args.output_file, all_evol_objs)
			utils.update_json_file(args.eliminated_file, all_pool_objs)

			# 途中結果出力
			new_cur_count = len(all_evol_objs[f"gen_{final_gen}"])
			print("{}件のInstructionを追加しました。".format(new_cur_count - cur_count))

			# 進捗バーを更新
			pbar.update(new_cur_count - cur_count)

			# 現状件数の更新
			cur_count = new_cur_count

			# 生成目標数に達したか確認
			if cur_count >= args.num_instructions_to_generate:
				print("目標数に達しました。ループを終了します。")
				break  # forループを抜ける


	# 進捗バーを完了
	pbar.close()

	# 結果出力
	final_count = len(all_evol_objs[f"gen_{final_gen}"])
	print("完了：{}件のInstructionを生成・追加しました。".format(final_count - first_count))
	print("　　　最終的なInstruction数は{}件です。".format(final_count))


if __name__ == "__main__":
	main()
