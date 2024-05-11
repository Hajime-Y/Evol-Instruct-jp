# ==============================
# 幅進化：問題のタイプを増やす
# ==============================
# v1
# base_instruction = "I want you act as a Prompt Creator.\n\
# Your goal is to draw inspiration from the #Given Prompt# to create a brand new prompt.\n\
# This new prompt should belong to the same domain as the #Given Prompt# but be even more rare.\n\
# The LENGTH and complexity of the #Created Prompt# should be similar to that of the #Given Prompt#.\n\
# The #Created Prompt# must be reasonable, easily understood and responded to by humans, and phrased naturally in Japanese, not in English.\n\
# '#Given Prompt#', '#Created Prompt#', 'given prompt' and 'created prompt' are not allowed to appear in #Created Prompt#\n"

# v1.1
# base_instruction = "I want you act as a Prompt Creator.\n\
# Your goal is to draw inspiration from the #Given Prompt# to create a brand new prompt.\n\
# This new prompt should has only one similarity to #Given Prompt#, but is much rarer.\n\
# The LENGTH and complexity of the #Created Prompt# should be similar to that of the #Given Prompt#.\n\
# The #Created Prompt# must be reasonable, easily understood and responded to by humans, and phrased naturally in Japanese, not in English.\n\
# '#Given Prompt#', '#Created Prompt#', 'given prompt' and 'created prompt' are not allowed to appear in #Created Prompt#\n"

# v1.2
# base_instruction = "I want you act as a Prompt Creator.\n\
# Your goal is to draw inspiration from the #Given Prompt# to create a brand new prompt.\n\
# The LENGTH and complexity of the #Created Prompt# should be similar to that of the #Given Prompt#.\n\
# The #Created Prompt# must be reasonable, easily understood and responded to by humans, and phrased naturally in Japanese, not in English.\n\
# '#Given Prompt#', '#Created Prompt#', 'given prompt' and 'created prompt' are not allowed to appear in #Created Prompt#\n"

# v1.3
# base_instruction = "I want you act as a Prompt Creator.\n\
# Your goal is to draw inspiration from the #Given Prompt# to create a brand new prompt.\n\
# This new prompt should be much rarer.\n\
# The LENGTH and complexity of the #Created Prompt# should be similar to that of the #Given Prompt#.\n\
# The #Created Prompt# must be reasonable, easily understood and responded to by humans, and phrased naturally in Japanese, not in English.\n\
# '#Given Prompt#', '#Created Prompt#', 'given prompt' and 'created prompt' are not allowed to appear in #Created Prompt#\n"

# v1.4
base_instruction = "I want you act as a Prompt Creator.\n\
Your goal is to draw inspiration from the #Given Prompt# to create a brand new prompt.\n\
This new prompt should be much rarer and it must be more natural Japanese.\n\
The LENGTH and complexity of the #Created Prompt# should be similar to that of the #Given Prompt#.\n\
The #Created Prompt# must be reasonable, easily understood and responded to by humans, must be more naturally Japanese, without English.\n\
'#Given Prompt#', '#Created Prompt#', 'given prompt' and 'created prompt' are not allowed to appear in #Created Prompt#\n"

# base_instruction = "プロンプト・クリエーターとして活動してほしい。\n\
# あなたのゴールは、#Given Prompt#からインスピレーションを得て、まったく新しいプロンプトを作成することです。\n\
# この新しいプロンプトは#Given Prompt#と同じ領域に属するものでなければならないが、さらに珍しいものでなければならない。\n\
# #Created Prompt#の長さと複雑さは、#Given Prompt#と同じでなければなりません。\n\
# #Created Prompt#は合理的でなければならず、人間が簡単に理解し応答できるものでなければならない。また、英語ではなく自然な日本語表現でなければならない。\n\
# '#Given Prompt#'と'#Created Prompt#'、'given prompt'、'created prompt'には#Created Prompt#を含めることができない。\n"


def createBreadthPrompt(instruction):
	prompt = base_instruction
	prompt += "#Given Prompt#: \n {} \n".format(instruction)
	prompt += "#Created Prompt#:\n"
	return prompt