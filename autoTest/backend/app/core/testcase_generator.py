from app.core.llm_client import LLMClient
from app.models.schemas import TestCase
import logging
import traceback
import uuid

# 配置日志记录器
logger = logging.getLogger(__name__)

class TestCaseGenerator:
    def __init__(self, model_name: str = "spark-max"):
        self.llm_client = LLMClient(model_name=model_name)
        
    async def generate_from_document(self, document_text: str) -> list[TestCase]:
        """
        从文档文本生成测试用例
        """
        try:
            logger.info("开始从文档生成测试用例")
            # 调用 LLMClient 生成测试用例
            test_cases = await self.llm_client.generate_test_cases(document_text)
            if not test_cases:
                logger.error("未生成测试用例")
                raise Exception("未生成测试用例")
            logger.info(f"成功生成 {len(test_cases)} 个测试用例")
            return test_cases
        except Exception as e:
            logger.error(f"生成测试用例失败: {str(e)}")
            logger.error(traceback.format_exc())
            raise Exception(f"生成测试用例失败: {str(e)}")
    
    def _validate_test_case(self, test_case: TestCase) -> bool:
        """
        验证测试用例的完整性
        """
        return all([
            test_case.title,
            test_case.description,
            test_case.steps,
            test_case.expected_result
        ]) 