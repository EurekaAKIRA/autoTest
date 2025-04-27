from pydantic import BaseModel
from typing import List

class TestCase(BaseModel):
    id: str
    title: str
    description: str
    steps: List[str]
    expected_result: str

class TestCaseResponse(BaseModel):
    message: str
    test_cases: List[TestCase] 