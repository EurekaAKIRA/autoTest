from app.core.testcase_generator import TestCaseGenerator
from app.utils.file_parser import parse_document

class GenerateService:
    def __init__(self):
        self.generator = TestCaseGenerator()
        
    async def generate_test_cases(self, file_content: bytes, file_type: str) -> list:
        """
        处理上传的文件并生成测试用例
        """
        # 解析文档
        document_text = parse_document(file_content, file_type)
        
        # 生成测试用例
        test_cases = await self.generator.generate_from_document(document_text)
        
        return test_cases 