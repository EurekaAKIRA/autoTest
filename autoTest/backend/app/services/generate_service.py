from app.core.testcase_generator import TestCaseGenerator
from app.utils.file_parser import parse_document
from app.models.schemas import TestCase
from pathlib import Path
import os
import logging
import traceback

# 配置日志记录器
logger = logging.getLogger(__name__)

# 使用与routes.py相同的上传目录
UPLOAD_DIR = Path("uploaded_files")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

class GenerateService:
    def __init__(self):
        self.testcase_generator = TestCaseGenerator()
        
    async def generate_test_cases(self, filename: str) -> list[TestCase]:
        """
        生成测试用例
        """
        try:
            logger.info(f"开始生成测试用例: {filename}")
            
            # 获取上传的文件路径
            file_path = UPLOAD_DIR / filename
            if not file_path.exists():
                logger.error(f"文件不存在: {filename}")
                raise Exception(f"文件不存在: {filename}")
                
            # 解析文档
            logger.info("开始解析文档")
            try:
                document_text = await parse_document(str(file_path))
                if not document_text:
                    logger.error("文档解析失败: 返回内容为空")
                    raise Exception("文档解析失败: 返回内容为空")
                logger.info(f"文档解析成功，文本长度: {len(document_text)}")
            except Exception as e:
                logger.error(f"文档解析失败: {str(e)}")
                logger.error(traceback.format_exc())
                raise Exception(f"文档解析失败: {str(e)}")
                
            # 生成测试用例
            logger.info("开始生成测试用例")
            try:
                test_cases = await self.testcase_generator.generate_from_document(document_text)
                if not test_cases:
                    logger.error("未生成测试用例")
                    raise Exception("未生成测试用例")
                logger.info(f"成功生成 {len(test_cases)} 个测试用例")
                return test_cases
            except Exception as e:
                logger.error(f"生成测试用例失败: {str(e)}")
                logger.error(traceback.format_exc())
                raise Exception(f"生成测试用例失败: {str(e)}")
        except Exception as e:
            logger.error(f"生成测试用例失败: {str(e)}")
            logger.error(traceback.format_exc())
            raise Exception(f"生成测试用例失败: {str(e)}") 