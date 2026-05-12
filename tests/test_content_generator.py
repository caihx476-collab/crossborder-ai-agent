import pytest
from unittest.mock import MagicMock, patch
from backend.services.content_generator import ContentGenerator
from backend.models.schemas import ProductInfo


class TestContentGenerator:
    @pytest.fixture
    def mock_provider(self):
        provider = MagicMock()
        provider.get_name.return_value = "TestProvider/test"
        return provider

    @pytest.fixture
    def product(self):
        return ProductInfo(name="Pet Water Fountain", feature="Ultra Silent", region="US", platform="amazon")

    def test_generate_titles(self, mock_provider, product):
        mock_provider.generate.return_value = '{"titles": ["Title 1", "Title 2", "Title 3", "Title 4", "Title 5"]}'
        gen = ContentGenerator(provider=mock_provider)
        titles = gen.generate_titles(product)
        assert len(titles) == 5
        assert titles[0] == "Title 1"

    def test_generate_keywords(self, mock_provider, product):
        mock_provider.generate.return_value = '{"keywords": ["kw1", "kw2", "kw3", "kw4", "kw5", "kw6", "kw7", "kw8", "kw9", "kw10"]}'
        gen = ContentGenerator(provider=mock_provider)
        keywords = gen.generate_keywords(product)
        assert len(keywords) == 10

    def test_generate_all(self, mock_provider, product):
        mock_provider.generate.side_effect = [
            '{"titles": ["T1", "T2", "T3", "T4", "T5"]}',
            '{"keywords": ["K1", "K2", "K3", "K4", "K5", "K6", "K7", "K8", "K9", "K10"]}',
        ]
        gen = ContentGenerator(provider=mock_provider)
        result = gen.generate_all(product, ["title", "seo"])
        assert len(result.items) == 15
        assert result.provider == "TestProvider/test"

    def test_parse_json_with_markdown(self, mock_provider, product):
        mock_provider.generate.return_value = '```json\n{"titles": ["T1"]}\n```'
        gen = ContentGenerator(provider=mock_provider)
        titles = gen.generate_titles(product)
        assert len(titles) == 1
