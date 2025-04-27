from fastapi.testclient import TestClient
from app.main import app
import pytest
from unittest.mock import patch, MagicMock
from app.models.schemas import TestCase

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "欢迎使用测试用例生成系统"}

@pytest.mark.asyncio
async def test_upload_document():
    # 模拟文件上传
    with patch('app.api.routes.generate_service') as mock_service:
        # 准备测试数据
        test_cases = [
            TestCase(
                id="test-id-1",
                title="测试用例1",
                description="测试描述",
                steps=["步骤1", "步骤2"],
                expected_result="预期结果"
            )
        ]
        
        # 模拟服务返回
        mock_service.generate_test_cases.return_value = test_cases
        
        # 准备测试文件
        files = {
            'file': ('test.docx', b'test content', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        }
        
        # 发送请求
        response = client.post("/api/upload", files=files)
        
        # 验证响应
        assert response.status_code == 200
        assert response.json()["message"] == "文件上传成功"
        assert len(response.json()["test_cases"]) == 1
        assert response.json()["test_cases"][0]["title"] == "测试用例1" 