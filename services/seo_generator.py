from services.ai_client import call_minimax


def build_prompt(product_info):
    prompt = f"""
你是一位资深亚马逊运营专家。

请根据以下商品信息生成10个英文SEO关键词。

商品名称：
{product_info["name"]}

商品特点：
{product_info["feature"]}

目标地区：
{product_info["region"]}

要求：
1. 每个关键词都和商品强相关
2. 面向Amazon搜索场景
3. 关键词自然，不要堆砌
4. 使用英文

请严格按照以下JSON格式输出：
{{
  "keywords": [
    "keyword1",
    "keyword2",
    "keyword3",
    "keyword4",
    "keyword5",
    "keyword6",
    "keyword7",
    "keyword8",
    "keyword9",
    "keyword10"
  ]
}}

不要输出任何解释文字。
"""
    return prompt


def generate_keywords(product_info):
    prompt = build_prompt(product_info)
    result = call_minimax(prompt)
    return result