import os
from pathlib import Path
from backend.utils.logger import logger


PROMPTS_DIR = Path(__file__).resolve().parent.parent.parent / "prompts"

PLATFORM_NAMES = {
    "amazon": "Amazon",
    "ebay": "eBay",
    "shopify": "Shopify",
}


class PromptBuilder:
    _cache: dict[str, str] = {}

    @classmethod
    def _load_template(cls, template_name: str) -> str:
        if template_name in cls._cache:
            return cls._cache[template_name]
        path = PROMPTS_DIR / template_name
        if not path.exists():
            raise FileNotFoundError(f"Prompt模板不存在: {path}")
        content = path.read_text(encoding="utf-8")
        cls._cache[template_name] = content
        return content

    @classmethod
    def build_title_prompt(cls, product_name: str, feature: str, region: str, platform: str = "amazon") -> str:
        platform_name = PLATFORM_NAMES.get(platform, platform)
        try:
            template = cls._load_template(f"title_{platform}.txt")
        except FileNotFoundError:
            template = cls._load_template("title_amazon.txt")
            logger.warning(f"平台 {platform} 无专用标题模板，使用amazon默认模板")

        return template.format(
            product_name=product_name,
            feature=feature,
            region=region,
            platform=platform_name,
        )

    @classmethod
    def build_seo_prompt(cls, product_name: str, feature: str, region: str, platform: str = "amazon") -> str:
        platform_name = PLATFORM_NAMES.get(platform, platform)
        try:
            template = cls._load_template(f"seo_{platform}.txt")
        except FileNotFoundError:
            template = cls._load_template("seo_amazon.txt")
            logger.warning(f"平台 {platform} 无专用SEO模板，使用amazon默认模板")

        return template.format(
            product_name=product_name,
            feature=feature,
            region=region,
            platform=platform_name,
        )

    @classmethod
    def build_description_prompt(cls, product_name: str, feature: str, region: str, platform: str = "amazon") -> str:
        platform_name = PLATFORM_NAMES.get(platform, platform)
        try:
            template = cls._load_template(f"description_{platform}.txt")
        except FileNotFoundError:
            template = cls._load_template("description_amazon.txt")
            logger.warning(f"平台 {platform} 无专用描述模板，使用amazon默认模板")

        return template.format(
            product_name=product_name,
            feature=feature,
            region=region,
            platform=platform_name,
        )
