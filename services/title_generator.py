from services.ai_client import call_minimax


def build_prompt(product_info):

    prompt = f"""
你是一位资深亚马逊运营专家。

请为以下商品生成5个英文商品标题。

商品名称：
{product_info["name"]}

商品特点：
{product_info["feature"]}

目标地区：
{product_info["region"]}

要求：
1. 符合Amazon SEO规则
2. 强调产品卖点
3. 标题自然
4. 返回JSON格式

请严格按照以下JSON格式输出：

{{
  "titles":[
    "title1",
    "title2",
    "title3",
    "title4",
    "title5"
  ]
}}

不要输出任何解释文字。
"""
    return prompt

def generate_title(product_info):

    prompt = build_prompt(product_info)
    result = call_minimax(prompt)
    return result
#自动重新生成函数
def regenerate_title(product_info, max_retry=3):

    for attempt in range(max_retry):

        result = generate_title(product_info)

        if len(result) < 1000:

            return result

    return "生成失败"