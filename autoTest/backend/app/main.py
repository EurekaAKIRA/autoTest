import logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s"
)

from fastapi import FastAPI
from app.database import engine, Base
from app import create_app

# 创建数据库表（不包含用户表）
Base.metadata.create_all(bind=engine)

app = create_app()

@app.get("/")
async def root():
    return {"message": "欢迎使用测试用例生成系统"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 