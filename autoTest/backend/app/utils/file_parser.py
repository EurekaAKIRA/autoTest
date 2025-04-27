from docx import Document
from pypdf import PdfReader
import io

def parse_document(file_content: bytes, file_type: str) -> str:
    """
    解析上传的文档文件，返回文本内容
    """
    if file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        return parse_word(file_content)
    elif file_type == "application/pdf":
        return parse_pdf(file_content)
    else:
        raise ValueError(f"不支持的文件类型: {file_type}")

def parse_word(file_content: bytes) -> str:
    """
    解析Word文档
    """
    doc = Document(io.BytesIO(file_content))
    return "\n".join([paragraph.text for paragraph in doc.paragraphs])

def parse_pdf(file_content: bytes) -> str:
    """
    解析PDF文档
    """
    pdf = PdfReader(io.BytesIO(file_content))
    text = ""
    for page in pdf.pages:
        text += page.extract_text() + "\n"
    return text 