from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path

def create_app() -> FastAPI:
    app = FastAPI()
    
    # 注册路由
    from app.api.routes import router as api_router
    app.include_router(api_router, prefix="/api")
    
    # 创建上传目录
    upload_dir = Path("uploaded_files")
    upload_dir.mkdir(parents=True, exist_ok=True)
    
    # 挂载静态文件目录
    app.mount("/uploads", StaticFiles(directory=str(upload_dir)), name="uploads")
    
    return app 