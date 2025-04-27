from openai import OpenAI
import os
from dotenv import load_dotenv
from app.models.schemas import TestCase
import uuid

load_dotenv()

class LLMClient:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
    async def generate_test_cases(self, document_text: str) -> list[TestCase]:
        """
        使用大模型生成测试用例
        """
        try:
            response = await self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": """你是一个专业的测试工程师。请根据提供的需求文档生成测试用例。
                        每个测试用例应包含以下内容：
                        1. 测试用例标题
                        2. 测试用例描述
                        3. 详细的测试步骤
                        4. 预期结果
                        
                        请以JSON格式返回测试用例列表，格式如下：
                        {
                            "test_cases": [
                                {
                                    "id": "唯一标识符",
                                    "title": "测试用例标题",
                                    "description": "测试用例描述",
                                    "steps": ["步骤1", "步骤2", ...],
                                    "expected_result": "预期结果"
                                }
                            ]
                        }"""
                    },
                    {
                        "role": "user",
                        "content": f"请根据以下需求文档生成测试用例：\n{document_text}"
                    }
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            # 解析响应并生成测试用例对象
            content = response.choices[0].message.content
            import json
            data = json.loads(content)
            
            return [
                TestCase(
                    id=str(uuid.uuid4()),
                    title=case["title"],
                    description=case["description"],
                    steps=case["steps"],
                    expected_result=case["expected_result"]
                )
                for case in data["test_cases"]
            ]
            
        except Exception as e:
            print(f"生成测试用例时发生错误: {str(e)}")
            return [] 