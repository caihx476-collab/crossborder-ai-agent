from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from backend.db.database import init_db
from backend.routers import generate, review, task, export
from backend.utils.exceptions import AppException
from backend.utils.logger import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 CrossBorder AI Agent 后端启动")
    init_db()
    yield
    logger.info("👋 CrossBorder AI Agent 后端关闭")


app = FastAPI(
    title="CrossBorder AI Agent",
    description="AI跨境电商运营助手后端API",
    version="2.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(generate.router)
app.include_router(review.router)
app.include_router(task.router)
app.include_router(export.router)


@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=500,
        content={"code": exc.code.value, "message": exc.message, "detail": exc.detail},
    )


@app.get("/api/health")
def health_check():
    return {"status": "ok", "version": "2.0.0"}
