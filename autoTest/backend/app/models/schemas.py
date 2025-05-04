from pydantic import BaseModel
from typing import List, Optional

class TestCase(BaseModel):
    id: str
    title: str
    description: str
    steps: List[str]
    expected_result: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "title": "测试用例标题",
                "description": "测试用例描述",
                "steps": ["步骤1", "步骤2", "步骤3"],
                "expected_result": "预期结果"
            }
        }

class TestCaseResponse(BaseModel):
    test_cases: List[TestCase]
    
    class Config:
        json_schema_extra = {
            "example": {
                "test_cases": [
                    {
                        "id": "123e4567-e89b-12d3-a456-426614174000",
                        "title": "测试用例标题",
                        "description": "测试用例描述",
                        "steps": ["步骤1", "步骤2", "步骤3"],
                        "expected_result": "预期结果"
                    }
                ]
            }
        }

class GenerateRequest(BaseModel):
    filename: str 