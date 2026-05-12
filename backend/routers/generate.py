from fastapi import APIRouter, HTTPException
from backend.models.schemas import GenerateRequest, GenerateResponse
from backend.services.content_generator import ContentGenerator
from backend.services.ai_provider import get_provider, AIProviderException
from backend.db.crud import save_task_and_items
from backend.utils.excel_exporter import export_to_excel
from backend.utils.logger import logger

router = APIRouter(prefix="/api", tags=["generate"])


@router.post("/generate", response_model=GenerateResponse)
def generate_content(req: GenerateRequest):
    try:
        provider = get_provider(req.provider)
        generator = ContentGenerator(provider=provider)
        response = generator.generate_all(req.product, req.content_types)

        excel_path = export_to_excel(
            [item.model_dump() for item in response.items],
            req.product.name,
        )

        save_task_and_items(
            response,
            product_name=req.product.name,
            product_feature=req.product.feature,
            region=req.product.region,
            platform=req.product.platform,
            excel_path=excel_path,
        )

        logger.info(f"内容生成完成: batch_id={response.batch_id}, provider={response.provider}")
        return response
    except AIProviderException as e:
        raise HTTPException(status_code=502, detail=e.message)
    except Exception as e:
        logger.error(f"内容生成失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))
