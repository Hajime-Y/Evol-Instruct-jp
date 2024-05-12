# ==============================
# 深さ進化：問題を少しだけ難しくする
# ==============================

# v1.0
# base_instruction = "I want you act as a Prompt Rewriter.\n \
# Your objective is to rewrite a given prompt into a more complex version to make those famous AI systems (e.g., chatgpt and GPT4) a bit harder to handle.\n \
# But the rewritten prompt must be reasonable, easily understood and responded to by humans, and must be more naturally Japanese, without English.\n \
# Your rewriting cannot omit the non-text parts such as the table and code in #The Given Prompt#:. Also, please do not omit the input in #The Given Prompt#. \n \
# You SHOULD complicate the given prompt using the following method: \n\
# {} \n\
# You should try your best not to make the #Rewritten Prompt# become verbose, #Rewritten Prompt# can only add 10 to 20 words into #The Given Prompt#. \n\
# '#The Given Prompt#', '#Rewritten Prompt#', 'given prompt' and 'rewritten prompt' are not allowed to appear in #Rewritten Prompt#\n"

# v1.1
base_instruction = "I want you act as a Prompt Rewriter.\n \
Your objective is to rewrite a given prompt into a more complex version to make those famous AI systems (e.g., chatgpt and GPT4) a bit harder to handle.\n \
But the rewritten prompt must be reasonable, easily understood and responded to by humans, and must be more naturally Japanese, without English.\n \
Your rewriting cannot omit the non-text parts such as the table and code in #The Given Prompt#:. Also, please do not omit the input in #The Given Prompt#. \n \
You SHOULD complicate the given prompt using the following method: \n\
{} \n\
You should try your best not to make the #Rewritten Prompt# become verbose, #Rewritten Prompt# can only add 10 to 20 words into #The Given Prompt#. \n\
You should try not to make one sentence too long in #Rewritten Prompt#. Long sentences should be broken up into multiple sentences to keep them readable. \n\
'#The Given Prompt#', '#Rewritten Prompt#', 'given prompt' and 'rewritten prompt' are not allowed to appear in #Rewritten Prompt#\n"

# base_instruction = "プロンプト・リライターとして活動してほしい。\n \
# あなたの目的は、与えられたプロンプトをより複雑なバージョンに書き換えて、有名なAIシステム（例：chatgptやGPT4）を少し扱いにくくすることだ。\n \
# しかし、書き換えられたプロンプトは合理的でなければならず、人間が簡単に理解し応答できなければならない。また、日本語でなければならない。\n \
# あなたの書き換えでは、#The Given Prompt#の表やコードなど、テキスト以外の部分を省略することはできません。また、#The Given Prompt#の入力も省略しないでください。 \n \
# 与えられたプロンプトを以下の方法で複雑にする必要があります: \n\
# {} \n\
# #Rewritten Prompt#が冗長にならないように努力すること。#Rewritten Prompt#は#The Given Prompt#に10語から20語程度しか追加できません。英語ではなく自然な日本語表現で書いてください。 \n\
# '#The Given Prompt#'と'#Rewritten Prompt#'、'given prompt'、'rewritten prompt'には#Rewritten Prompt#を含めることができない。\n"

def createConstraintsPrompt(instruction):
	prompt = base_instruction.format("Please add one more constraints/requirements into #The Given Prompt#'")
	prompt += "#The Given Prompt#: \n {} \n".format(instruction)
	prompt += "#Rewritten Prompt#:\n"
	return prompt

def createDeepenPrompt(instruction):
	prompt = base_instruction.format("If #The Given Prompt# contains inquiries about certain issues, the depth and breadth of the inquiry can be increased.")
	prompt += "#The Given Prompt#: \n {} \n".format(instruction)
	prompt += "#Rewritten Prompt#:\n"
	return prompt

def createConcretizingPrompt(instruction):
	prompt = base_instruction.format("Please replace general concepts with more specific concepts.")
	prompt += "#The Given Prompt#: \n {} \n".format(instruction)
	prompt += "#Rewritten Prompt#:\n"
	return prompt


def createReasoningPrompt(instruction):
	prompt = base_instruction.format("If #The Given Prompt# can be solved with just a few simple thinking processes, you can rewrite it to explicitly request multiple-step reasoning.")
	prompt += "#The Given Prompt#: \n {} \n".format(instruction)
	prompt += "#Rewritten Prompt#:\n"
	return prompt


base_input_instruction = "I want you act as a Prompt Rewriter.\n \
Your objective is to rewrite a given prompt into a more complex version using dataformat to make those famous AI systems (e.g., chatgpt and GPT4) more difficult to handle.\n \
But the rewritten prompt must be reasonable and must be understood and responded by humans, and must be more naturally Japanese, without English.\n \
You must add {} format text as input data in #Rewritten Prompt#\n \
You should try your best not to make the #Rewritten Prompt# become verbose, #Rewritten Prompt# can only add 10 to 20 words into #The Given Prompt#. \n\
You should try not to make one sentence too long in #Rewritten Prompt#. Long sentences should be broken up into multiple sentences to keep them readable. \n\
'#The Given Prompt#', '#Rewritten Prompt#', 'given prompt' and 'rewritten prompt' are not allowed to appear in #Rewritten Prompt#\n"


def createComplicateInputPrompt(instruction, data_format):
	prompt = base_input_instruction.format(data_format)
	prompt += "#The Given Prompt#: \n {} \n".format(instruction)
	prompt += "#Rewritten Prompt#:\n"
	return prompt
