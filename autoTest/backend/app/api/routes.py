from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.generate_service import GenerateService
from app.models.schemas import TestCaseResponse
from app.utils.file_parser import parse_document

router = APIRouter()
generate_service = GenerateService()

@router.post("/upload", response_model=TestCaseResponse)
async def upload_document(file: UploadFile = File(...)):
    """
    上传需求文档并生成测试用例
    """
    try:
        # 读取文件内容
        file_content = await file.read()
        
        # 生成测试用例
        test_cases = await generate_service.generate_test_cases(file_content, file.content_type)
        
        return {
            "message": "文件上传成功",
            "test_cases": test_cases
        }
    except ValueError as e:
        raise HTTPException(status_code=415, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"处理文件时发生错误: {str(e)}") 