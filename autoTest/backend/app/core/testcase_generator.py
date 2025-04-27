from app.core.llm_client import LLMClient
from app.models.schemas import TestCase

class TestCaseGenerator:
    def __init__(self):
        self.llm_client = LLMClient()
        
    async def generate_from_document(self, document_text: str) -> list[TestCase]:
        """
        从文档文本生成测试用例
        """
        # 调用大模型生成测试用例
        test_cases = await self.llm_client.generate_test_cases(document_text)
        
        # 验证生成的测试用例
        valid_cases = []
        for case in test_cases:
            if self._validate_test_case(case):
                valid_cases.append(case)
        
        return valid_cases
    
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