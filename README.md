# Evol-Instruct-jp

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

## Limitation

 - Mixtralの利用に[deepinfra](https://deepinfra.com/)というサービスの登録が必要です。
 - deepinfraのAPI Keyを取得し、Evol_Instruct_Japanese/config/secret_config.jsonを下記の形式で記載してください。
```
{
    "DEEPINFRA_API_KEY": "your_api_key",
}
```