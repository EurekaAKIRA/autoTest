# API 文档

## 基础信息
- 基础URL: `/api`
- 版本: 1.0.0

## 接口列表

### 1. 上传文档并生成测试用例

**请求**
- 方法: POST
- 路径: `/upload`
- 内容类型: multipart/form-data
- 参数:
  - file: 需求文档文件（支持Word和PDF格式）

**响应**
```json
{
    "message": "string",
    "test_cases": [
        {
            "id": "string",
            "title": "string",
            "description": "string",
            "steps": ["string"],
            "expected_result": "string"
        }
    ]
}
```

## 错误码
- 400: 请求参数错误
- 415: 不支持的文件类型
- 500: 服务器内部错误 