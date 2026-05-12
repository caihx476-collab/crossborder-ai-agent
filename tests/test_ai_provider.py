import pytest
from unittest.mock import patch, MagicMock
from backend.services.ai_provider import MiniMaxProvider, OpenAIProvider, OllamaProvider, get_provider
from backend.utils.exceptions import AIProviderException


class TestGetProvider:
    def test_get_minimax_provider(self):
        provider = get_provider("minimax")
        assert isinstance(provider, MiniMaxProvider)

    def test_get_openai_provider_without_key(self):
        with pytest.raises(AIProviderException, match="OPENAI_API_KEY"):
            get_provider("openai")

    def test_get_ollama_provider(self):
        provider = get_provider("ollama")
        assert isinstance(provider, OllamaProvider)

    def test_invalid_provider(self):
        with pytest.raises(AIProviderException):
            get_provider("invalid")


class TestMiniMaxProvider:
    def test_get_name(self):
        provider = MiniMaxProvider()
        assert "MiniMax" in provider.get_name()

    @patch("backend.services.ai_provider.MiniMaxProvider.generate")
    def test_generate_success(self, mock_generate):
        mock_generate.return_value = '{"titles": ["title1"]}'
        provider = MiniMaxProvider()
        result = provider.generate("test prompt")
        assert "title1" in result


class TestOllamaProvider:
    def test_get_name(self):
        provider = OllamaProvider()
        assert "Ollama" in provider.get_name()
