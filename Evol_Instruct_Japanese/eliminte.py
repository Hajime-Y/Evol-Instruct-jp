# ===============================
# Elimination Evolving. 以下の4つの状況を命令進化の失敗と分類する：
# 1. 進化した命令が、元の命令と比べて何の情報利得ももたらさない。この判定にはChatGPTを使用する。詳細は付録Gを参照。
# 2. 進化した命令は、LLMが応答を生成することを困難にする。私たちは、生成された応答が「ごめんなさい」を含み、比較的短い場合（つまり80語以下）、LLMが進化した指示に応答するのに苦労していることを示すことが多いことを発見した。そこで、このルールで判断することができる。
# 3. LLMが生成した応答には句読点とストップワードしか含まれていない。
# 4. 進化した命令は明らかに進化したプロンプトからいくつかの単語をコピーしている。例えば「与えられたプロンプト」、「書き直されたプロンプト」、「#書き直されたプロンプト#」など。
# ===============================
# 1.の中身は以下の通り
# ===============================

# 1.のプロンプト
eliminate_compare_prompt = """Here are two Instructions to ChatGPT AI, do you think they are equal to each other, which meet
the following requirements:
1. They have same constraints and requirments.
2. They have same depth and breadth of the inquiry.
The First Prompt: {first_instruction}
The Second Prompt: {second_instruction}
Your Judgement (Just answer: Equal or Not Equal. No need to explain the reason.):
"""

# eliminate_prompt = """ここにChatGPT AIへの2つの命令があります。
# 以下の条件を満たしています: 
# 1. 同じ制約と要求を持っている。
# 2. 質問の深さと幅が同じである。
# 最初のプロンプト: {これが最初の指示です。}
# 第二の命令: {これが2つ目の指示です。}
# あなたの判断（「同等か同等でないか」だけ答えてください）: 
# """

# 5. のプロンプト（追加）
# v1.0
eliminate_hallucination_prompt = """Evaluate the LLM instruction below to see if it:
1. It does not use non-existent words.
2. Relates to factual information for Japanese.
Prompt: {instruction}
Your Judgement (Just answer: True or False. No need to explain the reason.):
"""
# v1.1
# eliminate_hallucination_prompt = """Evaluate the prompt below to see if it:
# 1. It does not use non-existent words.
# 2. Relates to factual information in Japan.
# Returns True for mathematics, and programming tasks.
# Prompt: {instruction}
# Your Judgement (Just answer: True or False. No need to explain the reason.):
# """
# v1.2
# eliminate_hallucination_prompt = """Evaluate the prompt below to see if it:
# 1. It does not use non-existent words.
# 2. Is not a question that contains untrue information in Japan.
# Prompt: {instruction}
# Your Judgement (Just answer: True or False. No need to explain the reason. However, return True for math and programming tasks regardless of the above.):
# """

def createEliminateComparePrompt(instruction, evol_instruction):
    prompt = eliminate_compare_prompt.format(
        first_instruction=instruction, 
        second_instruction=evol_instruction
    )
    return prompt

def check_difficulty(response):
    """
    進化した命令がLLMにとって応答を生成することが困難かどうかを判断する関数。
    応答が「sorry」を含み、かつ80語以下である場合にTrueを返す。

    Args:
    response (str): LLMから生成された応答。

    Returns:
    bool: 応答が困難であるかどうかの真偽値。
    """
    return "sorry" in response and len(response.split()) < 80

def check_punctuation_stopwords(response, stop_words):
    """
    LLMが生成した応答が句読点とストップワードのみを含むかどうかを判断する関数。
    この関数は、応答が句読点とストップワードのみで構成されている場合にTrueを返す。

    Args:
    response (str): LLMから生成された応答。
    stop_words (set): 判定に使用するストップワードのセット。

    Returns:
    bool: 応答が句読点とストップワードのみで構成されているかどうかの真偽値。
    """
    words = response.split()
    return all(word.strip('.,!?:;()[]') in stop_words or not word.strip('.,!?:;()[]') for word in words)

def check_copied_words(evol_instruction):
    """
    進化した命令が進化するプロンプトからいくつかの単語を明らかにコピーしているかどうかを判断する関数。
    「given prompt」、「rewritten prompt」、「#Rewritten Prompt#」などの単語が含まれている場合にTrueを返す。

    Args:
    instruction (str): 元の命令。
    evol_instruction (str): 進化した命令。

    Returns:
    bool: 進化した命令が元の命令から単語をコピーしているかどうかの真偽値。
    """
    copied_phrases = ["given prompt", "rewritten prompt", "#Given Prompt#", "#Rewritten Prompt#"]
    return any(phrase in evol_instruction for phrase in copied_phrases)

def createEliminateHallucinationPrompt(instruction):
    prompt = eliminate_hallucination_prompt.format(
        instruction=instruction, 
    )
    return prompt