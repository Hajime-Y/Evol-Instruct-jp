# Evol-Instruct-jp

下記を参考にした、日本語でMixtral 8x22B Instructを使って合成データを作るためのコードです。  
 - report: [WizardLM: Empowering Large Language Models to Follow Complex Instructions](https://arxiv.org/abs/2304.12244)
 - reference: [WizardLMのEvol_Instruct](https://github.com/nlpxucan/WizardLM/tree/main/Evol_Instruct)

## Usage

1. 依存関係のインストール
```
poetry install
cd Evol_Instruct_Japanese
```

2. 進化の実行
```
python main.py \
    --input_file "./test_data/test.jsonl" \
	--output_file "./test_output/test_generated.json" \
	--eliminated_file "./test_output/test_eliminated.json" \
	--model "mistralai/Mixtral-8x22B-Instruct-v0.1" \
    --generations 4
```

### コマンドライン引数の詳細

- `--input_file`: 入力ファイルのパス。デフォルトは `./data/seed_tasks_jp_cleaned.jsonl` です。
- `--output_file`: 新しい世代の出力ファイルのパス。デフォルトは `./output/new_generation.json` です。
- `--eliminated_file`: 削除された項目の出力ファイルのパス。デフォルトは `./output/eliminated.json` です。
- `--model`: 使用するモデルの名前。デフォルトは `mistralai/Mixtral-8x22B-Instruct-v0.1` です。
- `--hallucination_check_model`: Instruction中に存在しない単語や概念がないかチェックするためのモデル。--modelとは異なるモデルを使用することを推奨します。デフォルトは `mistralai/Mixtral-8x7B-Instruct-v0.1` です。
- `--generations`: 進化する世代の数。デフォルトは 3 です。
- `--num_instructions_to_generate`: 最終世代で生成する指示の数。デフォルトは 10 です。
- `--subset_size`: 進化のためのデータセットのサブセットサイズを指定します。デフォルトは -1 で、この場合、データセット全体を使用します。seed taskが大規模の場合設定します。
- `--start_subset_index`: 進化を開始するサブセットのインデックス。デフォルトは 0 です。
- `--use_complicate_input_prompt`: 進化方法の一つとして複雑な入力プロンプトを使用するかどうか。数学的またはプログラミングのタスクに対して True に設定することを推奨します。


## Limitation

 - Mixtralの利用に[deepinfra](https://deepinfra.com/)というサービスの登録が必要です。
 - deepinfraのAPI Keyを取得し、Evol_Instruct_Japanese/config/secret_config.jsonを下記の形式で記載してください。
```
{
    "DEEPINFRA_API_KEY": "your_api_key",
}
```