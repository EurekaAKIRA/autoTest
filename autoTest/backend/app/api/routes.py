import os
from fastapi import APIRouter, UploadFile, File, HTTPException, Form, Request
from app.services.generate_service import GenerateService
from app.services.export_service import ExportService
from app.models.schemas import TestCaseResponse, TestCase
from app.utils.file_parser import parse_document
import shutil
from pathlib import Path
from fastapi.responses import StreamingResponse, JSONResponse
from docx import Document
import io
import logging
import traceback

# 配置日志记录器
logger = logging.getLogger(__name__)

router = APIRouter()
generate_service = GenerateService()
export_service = ExportService()
UPLOAD_DIR = Path("uploaded_files")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    上传文件
    """
    try:
        logger.info(f"开始上传文件: {file.filename}")
        
        # 检查文件类型
        if not file.filename:
            logger.error("文件名不能为空")
            raise HTTPException(status_code=400, detail="文件名不能为空")
            
        file_ext = Path(file.filename).suffix.lower()
        if file_ext not in ['.docx', '.pdf']:
            logger.error(f"不支持的文件类型: {file_ext}")
            raise HTTPException(status_code=400, detail="只支持上传Word和PDF文件")
            
        # 检查文件大小
        file_size = 0
        file_content = b''
        while chunk := await file.read(8192):
            file_size += len(chunk)
            file_content += chunk
            if file_size > 10 * 1024 * 1024:  # 10MB
                logger.error("文件大小超过限制")
                raise HTTPException(status_code=400, detail="文件大小不能超过10MB")
                
        logger.info(f"文件大小: {file_size} 字节")
        
        # 重置文件指针
        await file.seek(0)
        
        # 生成唯一文件名
        filename = file.filename
        counter = 1
        while (UPLOAD_DIR / filename).exists():
            name = Path(file.filename).stem
            ext = Path(file.filename).suffix
            filename = f"{name}_{counter}{ext}"
            counter += 1
            
        # 保存文件
        try:
            file_path = UPLOAD_DIR / filename
            with open(file_path, 'wb') as f:
                f.write(file_content)
            logger.info(f"文件保存成功: {filename}")
            return {"filename": filename}
        except Exception as e:
            logger.error(f"保存文件失败: {str(e)}")
            logger.error(traceback.format_exc())
            raise HTTPException(status_code=500, detail="保存文件失败")
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"上传文件失败: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate")
async def generate_test_cases(filename: str = Form(...)):
    """
    生成测试用例
    """
    try:
        logger.info(f"开始生成测试用例: {filename}")
        
        # 检查文件是否存在
        file_path = UPLOAD_DIR / filename
        if not file_path.exists():
            logger.error(f"文件不存在: {filename}")
            raise HTTPException(status_code=404, detail=f"文件不存在: {filename}")
            
        # 生成测试用例
        try:
            test_cases = await generate_service.generate_test_cases(filename)
            logger.info(f"成功生成 {len(test_cases)} 个测试用例")
            return {"test_cases": test_cases}
            
        except Exception as e:
            logger.error(f"生成测试用例失败: {str(e)}")
            logger.error(traceback.format_exc())
            raise HTTPException(status_code=500, detail=str(e))
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"生成测试用例失败: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/cleanup/{filename}")
async def cleanup_file(filename: str):
    """
    删除指定文件
    """
    try:
        logger.info(f"开始清理文件: {filename}")
        file_path = UPLOAD_DIR / filename
        
        if not file_path.exists():
            logger.error(f"文件不存在: {filename}")
            raise HTTPException(status_code=404, detail=f"文件不存在: {filename}")
            
        try:
            file_path.unlink()
            logger.info(f"文件删除成功: {filename}")
            return {"success": True}
        except Exception as e:
            logger.error(f"删除文件失败: {str(e)}")
            logger.error(traceback.format_exc())
            raise HTTPException(status_code=500, detail="删除文件失败")
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"清理文件失败: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/export_word")
async def export_word(test_cases: list[TestCase]):
    """
    导出Word文档
    """
    try:
        logger.info("开始导出Word文档")
        if not test_cases:
            logger.error("测试用例列表为空")
            raise HTTPException(status_code=400, detail="测试用例列表不能为空")
            
        try:
            docx_bytes = await export_service.export_to_word(test_cases)
            logger.info("Word文档导出成功")
            return StreamingResponse(
                io.BytesIO(docx_bytes),
                media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                headers={"Content-Disposition": "attachment; filename=test_cases.docx"}
            )
        except Exception as e:
            logger.error(f"导出Word文档失败: {str(e)}")
            logger.error(traceback.format_exc())
            raise HTTPException(status_code=500, detail="导出Word文档失败")
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"导出Word文档失败: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/export_script")
async def export_script(request: Request):
    """
    导出脚本
    """
    try:
        logger.info("开始导出脚本")
        # 从请求体中获取数据
        data = await request.json()
        test_cases_data = data.get("test_cases", [])
        script_type = data.get("script_type", "pytest")
        
        if not test_cases_data:
            logger.error("测试用例列表为空")
            raise HTTPException(status_code=400, detail="测试用例列表不能为空")
            
        # 将字典转换为TestCase对象
        test_cases = []
        for case_data in test_cases_data:
            test_case = TestCase(
                id=case_data.get("id", ""),
                title=case_data.get("title", ""),
                description=case_data.get("description", ""),
                steps=case_data.get("steps", []),
                expected_result=case_data.get("expected_result", "")
            )
            test_cases.append(test_case)
            
        try:
            script_content = await export_service.export_to_script(test_cases, script_type)
            logger.info("脚本导出成功")
            return StreamingResponse(
                io.BytesIO(script_content.encode()),
                media_type="text/plain",
                headers={"Content-Disposition": f"attachment; filename=test_script_{script_type}.py"}
            )
        except Exception as e:
            logger.error(f"导出脚本失败: {str(e)}")
            logger.error(traceback.format_exc())
            raise HTTPException(status_code=500, detail="导出脚本失败")
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"导出脚本失败: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e)) 