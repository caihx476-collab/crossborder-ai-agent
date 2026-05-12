import json


def parse_json(content):
    """
    把AI返回的JSON字符串
    转成Python字典
    """

    try:

        data = json.loads(content)

        return data

    except json.JSONDecodeError:

        print("JSON解析失败")

        return None