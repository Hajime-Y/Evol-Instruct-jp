import os
import json

def update_json_file(file_path, new_data):
    # 新しいデータでファイルを上書き保存
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(new_data, file, indent=4, ensure_ascii=False)


def load_json_file(file_path):
    """JSONファイルを読み込む関数"""
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError as e:
        print(f"{file_path}: {e}")
        raise e
    

def init_generation_keys(file_path, current_gen, final_gen):
    """ファイルに保存されている世代のキーを初期化し、期待される世代と一致するか確認する"""
    if os.path.exists(file_path):
        data = load_json_file(file_path)
        existing_gens = set(data.keys())
        expected_gens = {f"gen_{gen}" for gen in range(current_gen, final_gen + 1)}
        assert existing_gens == expected_gens, f"{file_path}に存在する世代{existing_gens}が想定される世代{expected_gens}と異なります。"
        return data
    else:
        return {f"gen_{gen}": [] for gen in range(current_gen, final_gen + 1)}