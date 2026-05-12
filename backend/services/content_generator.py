import json
from datetime import datetime
from typing import Optional
from backend.services.ai_provider import AIProvider, get_provider
from backend.services.prompt_builder import PromptBuilder
from backend.models.schemas import ProductInfo, ContentItem, GenerateResponse
from backend.utils.logger import logger
from backend.utils.exceptions import AIResponseParseException


class ContentGenerator:
    def __init__(self, provider: Optional[AIProvider] = None):
        self.provider = provider or get_provider()

    def _parse_json(self, raw: str) -> dict:
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            for start, end in [("{", "}"), ("[", "]")]:
                s = raw.find(start)
                e = raw.rfind(end)
                if s != -1 and e != -1:
                    try:
                        return json.loads(raw[s : e + 1])
                    except json.JSONDecodeError:
                        continue
            raise AIResponseParseException("AI返回内容无法解析为JSON", raw[:200])

    def _call_with_retry(self, prompt: str, max_retry: int = 3) -> str:
        for attempt in range(max_retry):
            try:
                result = self.provider.generate(prompt)
                if result and len(result) > 10:
                    return result
                logger.warning(f"第{attempt+1}次生成结果异常，正在重试...")
            except Exception as e:
                if attempt == max_retry - 1:
                    raise
                logger.warning(f"第{attempt+1}次调用失败: {e}，正在重试...")
        raise AIResponseParseException("多次重试后仍无法生成有效内容")

    def generate_titles(self, product: ProductInfo) -> list[str]:
        prompt = PromptBuilder.build_title_prompt(
            product.name, product.feature, product.region, product.platform
        )
        raw = self._call_with_retry(prompt)
        data = self._parse_json(raw)
        titles = data.get("titles", [])
        if not titles:
            raise AIResponseParseException("AI未返回标题数据", raw[:200])
        logger.info(f"生成 {len(titles)} 个标题")
        return titles

    def generate_keywords(self, product: ProductInfo) -> list[str]:
        prompt = PromptBuilder.build_seo_prompt(
            product.name, product.feature, product.region, product.platform
        )
        raw = self._call_with_retry(prompt)
        data = self._parse_json(raw)
        keywords = data.get("keywords", [])
        if not keywords:
            raise AIResponseParseException("AI未返回关键词数据", raw[:200])
        logger.info(f"生成 {len(keywords)} 个关键词")
        return keywords

    def generate_descriptions(self, product: ProductInfo) -> list[str]:
        prompt = PromptBuilder.build_description_prompt(
            product.name, product.feature, product.region, product.platform
        )
        raw = self._call_with_retry(prompt)
        data = self._parse_json(raw)
        descriptions = data.get("descriptions", [])
        if not descriptions:
            raise AIResponseParseException("AI未返回描述数据", raw[:200])
        logger.info(f"生成 {len(descriptions)} 个描述")
        return descriptions

    def generate_all(self, product: ProductInfo, content_types: list[str]) -> GenerateResponse:
        batch_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        items: list[ContentItem] = []

        if "title" in content_types:
            titles = self.generate_titles(product)
            for i, title in enumerate(titles):
                items.append(ContentItem(
                    item_id=f"{batch_id}_title_{i+1}",
                    batch_id=batch_id,
                    item_type="Title",
                    content=title,
                    status="Pending",
                    created_at=created_at,
                ))

        if "seo" in content_types:
            keywords = self.generate_keywords(product)
            for i, kw in enumerate(keywords):
                items.append(ContentItem(
                    item_id=f"{batch_id}_keyword_{i+1}",
                    batch_id=batch_id,
                    item_type="SEO Keyword",
                    content=kw,
                    status="Pending",
                    created_at=created_at,
                ))

        if "description" in content_types:
            descriptions = self.generate_descriptions(product)
            for i, desc in enumerate(descriptions):
                items.append(ContentItem(
                    item_id=f"{batch_id}_desc_{i+1}",
                    batch_id=batch_id,
                    item_type="Description",
                    content=desc,
                    status="Pending",
                    created_at=created_at,
                ))

        return GenerateResponse(
            batch_id=batch_id,
            items=items,
            provider=self.provider.get_name(),
            created_at=created_at,
        )
