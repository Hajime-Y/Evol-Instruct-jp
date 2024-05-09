"""
main.py

run:
python main.py \
	--input_file "./data/seed_tasks_jp_cleaned.jsonl" \
	--output_file "./output/new_generation.json" \
	--eliminated_file "./output/eliminated.json" \
	--model "mistralai/Mixtral-8x22B-Instruct-v0.1"
"""

import json
import argparse
from tqdm.auto import tqdm

from evol_instruct import evol_instruct


def parse_arguments():
	"""引数を設定"""
	parser = argparse.ArgumentParser(description='Process some integers.')
	parser.add_argument('--input_file', type=str, default='./data/seed_tasks_jp_cleaned.jsonl', help='Input file path')
	parser.add_argument('--output_file', type=str, default='./output/new_generation.json', help='Output file path for new generations')
	parser.add_argument('--eliminated_file', type=str, default='./output/eliminated.json', help='Output file path for eliminated items')
	parser.add_argument('--model', type=str, default='mistralai/Mixtral-8x22B-Instruct-v0.1', help='model name')
	parser.add_argument('--generations', type=int, default=1, help='Number of generations to evolve')
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

	# 複数回Instruction進化
	all_evol_objs = {f"gen_{cur_gen}": all_objs}  # 保存用辞書(全世代)
	all_pool_objs = {}  # 失敗したInstructionの退避用辞書(全世代)
	for _ in tqdm(range(args.generations)):
		# Instructionの進化
		evol_objs, pool_objs, gen_number = evol_instruct(
			all_objs, 
			model=model, 
			stop_words=stop_words,
		)
		# 格納
		all_evol_objs[f"gen_{gen_number}"] = evol_objs
		all_pool_objs[f"gen_{gen_number}"] = pool_objs
		# 次の世代の元を入れ替え
		all_objs = evol_objs


	# 結果出力
	with open(args.output_file, 'w') as f:    
		json.dump(all_evol_objs, f, indent=4, ensure_ascii=False)
	with open(args.eliminated_file, 'w') as f:    
		json.dump(all_pool_objs, f, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    main()