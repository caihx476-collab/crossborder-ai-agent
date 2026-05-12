from fastapi import APIRouter, HTTPException
from backend.models.schemas import BatchReviewRequest
from backend.db.crud import update_item_status, batch_update_status, get_items_by_batch
from backend.utils.exceptions import NotFoundException
from backend.utils.logger import logger

router = APIRouter(prefix="/api", tags=["review"])

STATUS_MAP = {
    "approve": "Approved",
    "reject": "Rejected",
    "restore": "Pending",
}


@router.put("/items/{item_id}/status")
def update_status(item_id: str, action: str):
    new_status = STATUS_MAP.get(action)
    if not new_status:
        raise HTTPException(status_code=400, detail=f"无效操作: {action}")
    try:
        update_item_status(item_id, new_status)
        return {"item_id": item_id, "status": new_status}
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=e.message)


@router.post("/items/batch-review")
def batch_review(req: BatchReviewRequest):
    updates = []
    for item in req.items:
        new_status = STATUS_MAP.get(item.action)
        if not new_status:
            continue
        updates.append({"item_id": item.item_id, "status": new_status})
    if updates:
        batch_update_status(updates)
    return {"updated": len(updates)}


@router.get("/tasks/{batch_id}/items")
def get_task_items(batch_id: str):
    try:
        items = get_items_by_batch(batch_id)
        return {"items": [item.model_dump() for item in items]}
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=e.message)
