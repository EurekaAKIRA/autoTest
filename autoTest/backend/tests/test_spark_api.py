from sparkai.llm.llm import ChatSparkLLM, ChunkPrintHandler
from sparkai.core.messages import ChatMessage
import os
from dotenv import load_dotenv
import pytest
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 加载环境变量
load_dotenv()

# 配置参数
SPARKAI_URL = 'wss://spark-api.xf-yun.com/v3.5/chat'
SPARKAI_APP_ID = os.getenv("SPARK_APP_ID")
SPARKAI_API_KEY = os.getenv("SPARK_API_KEY")
SPARKAI_API_SECRET = os.getenv("SPARK_API_SECRET")
SPARKAI_DOMAIN = 'generalv3.5'

@pytest.mark.asyncio
async def test_spark_api_connection():
    """测试讯飞星火API的连通性"""
    try:
        logger.info("开始测试讯飞星火API...")
        logger.info(f"APP_ID: {SPARKAI_APP_ID}")
        logger.info(f"API_KEY: {SPARKAI_API_KEY}")
        logger.info(f"API_SECRET: {SPARKAI_API_SECRET}")
        
        # 初始化客户端
        spark = ChatSparkLLM(
            spark_api_url=SPARKAI_URL,
            spark_app_id=SPARKAI_APP_ID,
            spark_api_key=SPARKAI_API_KEY,
            spark_api_secret=SPARKAI_API_SECRET,
            spark_llm_domain=SPARKAI_DOMAIN,
            streaming=False,
        )
        
        # 准备消息
        messages = [ChatMessage(
            role="user",
            content="你好，请简单介绍一下你自己"
        )]
        
        # 设置回调处理器
        handler = ChunkPrintHandler()
        
        # 发送请求
        logger.info("发送请求...")
        response = spark.generate([messages], callbacks=[handler])
        
        # 打印结果
        logger.info("API响应:")
        logger.info(response)
        
        # 验证响应
        assert response is not None
        assert len(response) > 0
        
    except Exception as e:
        logger.error(f"测试失败，错误信息: {str(e)}")
        logger.error("详细错误:")
        import traceback
        logger.error(traceback.format_exc())
        raise

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_spark_api_connection()) 