from abc import ABC, abstractmethod
from backend.utils.logger import logger
from backend.utils.exceptions import AIProviderException, AITimeoutException
from backend.config import settings


class AIProvider(ABC):
    @abstractmethod
    def generate(self, prompt: str) -> str:
        ...

    @abstractmethod
    def get_name(self) -> str:
        ...


class MiniMaxProvider(AIProvider):
    def __init__(self):
        import requests
        self._requests = requests
        self.api_key = settings.MINIMAX_API_KEY
        self.model = settings.MINIMAX_MODEL
        if not self.api_key:
            raise AIProviderException("MINIMAX_API_KEY 未配置")

    def get_name(self) -> str:
        return f"MiniMax/{self.model}"

    def generate(self, prompt: str) -> str:
        url = "https://api.minimax.chat/v1/text/chatcompletion_v2"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7,
        }
        try:
            resp = self._requests.post(url, headers=headers, json=payload, timeout=60)
            resp.raise_for_status()
            result = resp.json()
            content = result["choices"][0]["message"]["content"]
            return content.replace("```json", "").replace("```", "").strip()
        except self._requests.exceptions.Timeout:
            raise AITimeoutException("MiniMax API 请求超时")
        except self._requests.exceptions.SSLError:
            raise AIProviderException("MiniMax API SSL连接失败", "请检查VPN/代理/网络环境")
        except Exception as e:
            raise AIProviderException(f"MiniMax API 调用失败: {e}")


class OpenAIProvider(AIProvider):
    def __init__(self):
        from openai import OpenAI
        self.api_key = settings.OPENAI_API_KEY
        self.model = settings.OPENAI_MODEL
        if not self.api_key:
            raise AIProviderException("OPENAI_API_KEY 未配置")
        self._client = OpenAI(api_key=self.api_key)

    def get_name(self) -> str:
        return f"OpenAI/{self.model}"

    def generate(self, prompt: str) -> str:
        try:
            response = self._client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
            )
            content = response.choices[0].message.content
            return content.replace("```json", "").replace("```", "").strip()
        except Exception as e:
            raise AIProviderException(f"OpenAI API 调用失败: {e}")


class OllamaProvider(AIProvider):
    def __init__(self):
        self.base_url = settings.OLLAMA_BASE_URL.rstrip("/")
        self.model = settings.OLLAMA_MODEL

    def get_name(self) -> str:
        return f"Ollama/{self.model}"

    def generate(self, prompt: str) -> str:
        import httpx
        try:
            resp = httpx.post(
                f"{self.base_url}/api/generate",
                json={"model": self.model, "prompt": prompt, "stream": False},
                timeout=120,
            )
            resp.raise_for_status()
            content = resp.json().get("response", "")
            return content.replace("```json", "").replace("```", "").strip()
        except httpx.TimeoutException:
            raise AITimeoutException("Ollama 请求超时")
        except Exception as e:
            raise AIProviderException(f"Ollama 调用失败: {e}")


_PROVIDERS = {
    "minimax": MiniMaxProvider,
    "openai": OpenAIProvider,
    "ollama": OllamaProvider,
}


def get_provider(name: str | None = None) -> AIProvider:
    provider_name = name or settings.AI_PROVIDER
    if provider_name not in _PROVIDERS:
        raise AIProviderException(f"不支持的AI模型: {provider_name}")
    logger.info(f"使用AI模型: {provider_name}")
    return _PROVIDERS[provider_name]()
