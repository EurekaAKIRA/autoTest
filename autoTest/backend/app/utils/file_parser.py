from docx import Document
from pypdf import PdfReader
import io
import traceback
from pathlib import Path
import logging

# 配置日志记录器
logger = logging.getLogger(__name__)

async def parse_document(file_path: str) -> str:
    """
    解析上传的文档文件，返回文本内容
    """
    try:
        logger.info(f"开始解析文档: {file_path}")
        file_path = Path(file_path)
        
        if not file_path.exists():
            logger.error(f"文件不存在: {file_path}")
            raise ValueError(f"文件不存在: {file_path}")
            
        # 读取文件内容
        with open(file_path, 'rb') as f:
            content = f.read()
            
        if not content:
            logger.error("文件内容为空")
            raise ValueError("文件内容为空")
            
        logger.info(f"文件大小: {len(content)} 字节")
        
        # 根据文件类型解析
        if file_path.suffix.lower() == '.docx':
            return parse_word(content)
        elif file_path.suffix.lower() == '.pdf':
            return parse_pdf(content)
        else:
            logger.error(f"不支持的文件类型: {file_path.suffix}")
            raise ValueError(f"不支持的文件类型: {file_path.suffix}")
    except Exception as e:
        logger.error(f"解析文档失败: {str(e)}")
        logger.error(traceback.format_exc())
        raise ValueError(f"解析文档失败: {str(e)}")

def parse_word(content: bytes) -> str:
    """
    解析Word文档
    """
    try:
        logger.info("开始解析Word文档")
        doc = Document(io.BytesIO(content))
        text = []
        for para in doc.paragraphs:
            if para.text.strip():
                text.append(para.text)
        result = '\n'.join(text)
        logger.info(f"Word文档解析成功，文本长度: {len(result)}")
        return result
    except Exception as e:
        logger.error(f"解析Word文档失败: {str(e)}")
        logger.error(traceback.format_exc())
        raise ValueError(f"解析Word文档失败: {str(e)}")

def parse_pdf(content: bytes) -> str:
    """
    解析PDF文档
    """
    try:
        logger.info("开始解析PDF文档")
        pdf = PdfReader(io.BytesIO(content))
        text = []
        for page in pdf.pages:
            text.append(page.extract_text())
        result = '\n'.join(text)
        logger.info(f"PDF文档解析成功，文本长度: {len(result)}")
        return result
    except Exception as e:
        logger.error(f"解析PDF文档失败: {str(e)}")
        logger.error(traceback.format_exc())
        raise ValueError(f"解析PDF文档失败: {str(e)}") 