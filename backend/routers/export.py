from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from backend.db.crud import get_items_by_batch
from backend.utils.excel_exporter import export_to_excel
from backend.utils.exceptions import NotFoundException
from backend.utils.logger import logger

router = APIRouter(prefix="/api", tags=["export"])


@router.get("/export/{batch_id}")
def export_excel(batch_id: str):
    try:
        items = get_items_by_batch(batch_id)
        item_dicts = [item.model_dump() for item in items]
        product_name = batch_id
        excel_path = export_to_excel(item_dicts, product_name)
        if not excel_path:
            raise HTTPException(status_code=500, detail="Excel导出失败")
        return FileResponse(
            excel_path,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            filename=excel_path.split("/")[-1].split("\\")[-1],
        )
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=e.message)
