import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("MINIMAX_API_KEY")


def call_minimax(prompt):
    """
    调用 MiniMax API，并返回 AI 生成的文本内容
    """

    url = "https://api.minimax.chat/v1/text/chatcompletion_v2"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "MiniMax-M2.7",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.7
    }

    try:
        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=60
        )

        result = response.json()

        content = result["choices"][0]["message"]["content"]

        clean_content = content.replace("```json", "").replace("```", "").strip()

        return clean_content

    except requests.exceptions.SSLError:
        return "API连接失败：SSL网络连接中断，请稍后重试，或检查VPN/代理/网络环境。"

    except requests.exceptions.Timeout:
        return "API连接失败：请求超时，请稍后重试。"

    except Exception as e:
        return f"API调用失败：{e}"