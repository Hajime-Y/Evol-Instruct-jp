import requests
from openai import OpenAI, OpenAIError
import time
import json


with open('config/secret_config.json') as f:
    config = json.load(f)

openai = OpenAI(
    api_key=config['DEEPINFRA_API_KEY'],
    base_url="https://api.deepinfra.com/v1/openai",
)


def get_oai_completion(
        prompt, 
        model="mistralai/Mixtral-8x22B-Instruct-v0.1",
        temperature=0.9,
        top_p=1.0,
        max_tokens=1024,
        stop=None,
        n=1
    ):

    try: 
        response = openai.chat.completions.create(
			model=model,
			messages=[
					{"role": "system", "content": "You are a helpful Japanese assistant."},
					{"role": "user", "content": prompt},
				],
			temperature=temperature,
			max_tokens=max_tokens,
			top_p=top_p,
			stop=stop,
		)
        return response.choices[0].message.content
    except requests.exceptions.Timeout as e:
        # Handle the timeout error here
        print("The API request timed out. Please try again later.")
        raise e
    except OpenAIError as e:
        print(f"OpenAIError: {e}.")
        raise e


def call_chatmodel(instruction, model_name="mistralai/Mixtral-8x22B-Instruct-v0.1"):
    success = False
    re_try_count = 5
    ans = ''
    while not success and re_try_count >= 0:
        re_try_count -= 1
        try:
            ans = get_oai_completion(
                instruction, 
                model=model_name,
                temperature=0.8,
                top_p=0.95,
            )
            success = True
        except:
            time.sleep(2)
            print('retry for sample:', instruction)
    return ans


def compare_evol_instructions(prompt, model_name="mistralai/Mixtral-8x22B-Instruct-v0.1"):
    """
    データに対してチェックを行い、結果をbool値で返す。

    Args:
    prompt (str): チェック用のプロンプト

    Returns:
    bool: チェックの結果(Equal: True, Not Equal: False)
    """
    # 最大5回確認
    for _ in range(5):
        try:
            check_result = get_oai_completion(
                prompt, 
                model=model_name,
                max_tokens=3,
            )
            # print(f"check_result: {check_result}")
            # resultを返す(TrueとFalseのどちらか)
            if "Not Equal" in check_result:
                return False
            elif "Equal" in check_result:
                return True
            else:
                continue
        except Exception as e:
            print(f"Error: {e}")
        time.sleep(2)  # リクエストレートリミットのために一時停止
    # 最大数確認しても結果が不明な場合、Falseとする
    return False
    

def check_hallucination(prompt, model_name="mistralai/Mixtral-8x7B-Instruct-v0.1"):
    """
    データに対してチェックを行い、結果をbool値で返す。

    Args:
    prompt (str): チェック用のプロンプト

    Returns:
    bool: チェックの結果(ハルシネーションなし: True, ハルシネーションあり: False)
    """
    # 最大5回確認
    for _ in range(5):
        try:
            check_result = get_oai_completion(
                prompt, 
                model=model_name,
                max_tokens=3,
                # temperature=1.0,
                # top_p=0.95,
            )
            # resultを返す(TrueとFalseのどちらか)
            if "False" in check_result and "True" not in check_result:
                print("check_hallucination: False")
                print(f"  {prompt}")
                print(f"check_result: {check_result}")
                return False
            elif "True" in check_result and "False" not in check_result:
                return True
            else:
                continue
        except Exception as e:
            print(f"Error: {e}")
        time.sleep(2)  # リクエストレートリミットのために一時停止
    # 最大数確認しても結果が不明な場合、Falseとする
    return False