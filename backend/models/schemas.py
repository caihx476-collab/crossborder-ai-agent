from pydantic import BaseModel, Field
from typing import Literal, Optional
from datetime import datetime


class ProductInfo(BaseModel):
    name: str = Field(..., min_length=1, description="商品名称")
    feature: str = Field(..., min_length=1, description="商品特点")
    region: str = Field(default="US", description="目标地区")
    platform: Literal["amazon", "ebay", "shopify"] = Field(default="amazon", description="目标平台")


class GenerateRequest(BaseModel):
    product: ProductInfo
    content_types: list[Literal["title", "seo", "description"]] = Field(default=["title", "seo"])
    provider: Optional[Literal["minimax", "openai", "ollama"]] = None


class ContentItem(BaseModel):
    item_id: str
    batch_id: str
    item_type: Literal["Title", "SEO Keyword", "Description"]
    content: str
    status: Literal["Pending", "Approved", "Rejected"] = "Pending"
    created_at: Optional[str] = None


class GenerateResponse(BaseModel):
    batch_id: str
    items: list[ContentItem]
    provider: str
    created_at: str


class ReviewAction(BaseModel):
    item_id: str
    action: Literal["approve", "reject", "restore"]


class BatchReviewRequest(BaseModel):
    items: list[ReviewAction]


class TaskSummary(BaseModel):
    batch_id: str
    product_name: str
    region: str
    platform: str
    total_items: int
    pending_count: int
    approved_count: int
    rejected_count: int
    created_at: str
    excel_path: Optional[str] = None


class DashboardStats(BaseModel):
    total_tasks: int
    total_items: int
    pending_count: int
    approved_count: int
    rejected_count: int
