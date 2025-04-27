from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="测试用例生成系统",
    description="基于大模型的测试用例自动生成系统",
    version="1.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该限制为特定域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 导入路由
from app.api.routes import router as api_router
app.include_router(api_router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "欢迎使用测试用例生成系统"} 