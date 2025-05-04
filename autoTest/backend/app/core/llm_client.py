import os
from dotenv import load_dotenv
from app.models.schemas import TestCase
import uuid
import json
import traceback
from typing import Optional
import time
import hmac
import hashlib
import base64
import websockets
import asyncio
from email.utils import formatdate
from urllib.parse import quote
import re
from datetime import datetime

load_dotenv()

class LLMClient:
    def __init__(self, model_name: str = "spark-max"):
        self.app_id = os.getenv("SPARK_APP_ID")
        self.api_key = os.getenv("SPARK_API_KEY")
        self.api_secret = os.getenv("SPARK_API_SECRET")
        
        if not all([self.app_id, self.api_key, self.api_secret]):
            raise ValueError("未设置讯飞星火 API 相关环境变量")
            
        self.model_name = model_name
        self.domain = "generalv3.5"  # Spark Max 版本
        self.max_retries = 3  # 最大重试次数
        self.retry_delay = 2  # 重试延迟（秒）
        
    def _create_url(self):
        """
        生成讯飞星火 WebSocket 鉴权url（严格按官方文档，适配Spark Max）
        """
        # 使用当前UTC时间
        current_time = datetime.utcnow()
        gmt_date = current_time.strftime("%a, %d %b %Y %H:%M:%S GMT")
        
        # 生成签名原始字符串
        host = "spark-api.xf-yun.com"
        path = "/v3.5/chat"
        request_line = f"GET {path} HTTP/1.1"
        
        signature_origin = f"host: {host}\n"
        signature_origin += f"date: {gmt_date}\n"
        signature_origin += request_line
        
        print("签名原始字符串:", signature_origin)
        
        # 使用 HMAC-SHA256 算法生成签名
        signature_sha = hmac.new(
            self.api_secret.encode('utf-8'),
            signature_origin.encode('utf-8'),
            hashlib.sha256
        ).digest()
        
        # Base64 编码签名
        signature = base64.b64encode(signature_sha).decode('utf-8')
        
        # 生成 authorization 参数
        authorization_origin = f'api_key="{self.api_key}", algorithm="hmac-sha256", headers="host date request-line", signature="{signature}"'
        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode('utf-8')
        
        # 生成 WebSocket URL（严格按照文档顺序）
        url = f"wss://{host}{path}"
        url += f"?host={host}"
        url += f"&date={quote(gmt_date)}"
        url += f"&authorization={authorization}"
        
        # 打印调试信息
        print("当前UTC时间:", gmt_date)
        print("API Key:", self.api_key)
        print("生成的签名:", signature)
        print("WebSocket URL:", url)
        print("authorization原文：", authorization_origin)
        
        return url
        
    async def _retry_with_backoff(self, func, *args, **kwargs):
        """
        带退避的重试机制
        """
        last_error = None
        for attempt in range(self.max_retries):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                last_error = e
                if attempt == self.max_retries - 1:
                    print(f"所有重试都失败了，最后一次错误: {str(e)}")
                    raise
                wait_time = self.retry_delay * (2 ** attempt)  # 指数退避
                print(f"尝试 {attempt + 1} 失败，{wait_time} 秒后重试... 错误: {str(e)}")
                await asyncio.sleep(wait_time)
                
    async def generate_test_cases(self, document_text: str) -> list[TestCase]:
        """
        使用讯飞星火大模型生成测试用例
        """
        if not document_text:
            raise Exception("文档内容为空")
            
        try:
            print(f"正在调用讯飞星火 API 生成测试用例 (模型: {self.model_name})...")
            print(f"文档长度: {len(document_text)} 字符")
            
            url = self._create_url()
            print("完整的 WebSocket URL:", url)
            
            # 构建请求数据
            data = {
                "header": {
                    "app_id": self.app_id,
                    "uid": "testuser"
                },
                "parameter": {
                    "chat": {
                        "domain": self.domain,
                        "temperature": 0.7,
                        "max_tokens": 2000
                    }
                },
                "payload": {
                    "message": {
                        "text": [
                            {
                                "role": "system",
                                "content": (
                                    "你是一名资深的软件测试工程师。请根据用户提供的需求文档，生成结构化、详细且专业的测试用例。每个测试用例应包含以下字段：\n"
                                    "- 标题（title）：简明描述测试目标\n"
                                    "- 描述（description）：详细说明测试目的和背景\n"
                                    "- 步骤（steps）：分步骤详细列出操作流程，每一步为一句话，不要带编号\n"
                                    "- 预期结果（expected_result）：每个测试用例的最终预期结果\n"
                                    "请以如下 JSON 格式返回（不要添加多余说明或代码块标记）：\n"
                                    "{\n  \"test_cases\": [\n    {\n      \"title\": \"测试用例标题\",\n      \"description\": \"测试用例描述\",\n      \"steps\": [\n        \"步骤1内容\",\n        \"步骤2内容\"\n      ],\n      \"expected_result\": \"预期结果内容\"\n    }\n  ]\n}\n如有多个测试点，请生成多个测试用例。"
                                )
                            },
                            {
                                "role": "user",
                                "content": f"请根据以下需求文档生成测试用例：\n{document_text}"
                            }
                        ]
                    }
                }
            }
            
            print("发送到讯飞星火的数据：", json.dumps(data, ensure_ascii=False, indent=2))
            
            async with websockets.connect(url, ping_interval=30, ping_timeout=10) as websocket:
                await websocket.send(json.dumps(data))
                
                all_contents = []
                while True:
                    response = await websocket.recv()
                    print("收到原始响应：", response)
                    response_data = json.loads(response)
                    
                    # 检查响应状态
                    if response_data["header"].get("code") != 0:
                        error_msg = response_data["header"].get("message", "未知错误")
                        raise Exception(f"API返回错误: {error_msg}")
                        
                    # 收集 assistant 的内容
                    if (
                        "payload" in response_data and
                        "choices" in response_data["payload"] and
                        "text" in response_data["payload"]["choices"]
                    ):
                        for item in response_data["payload"]["choices"]["text"]:
                            if item.get("role") == "assistant":
                                all_contents.append(item.get("content", ""))
                                
                    # 判断是否为最后一包
                    if response_data["header"].get("status") == 2:
                        break
                        
                content = "".join(all_contents)
                if not content:
                    raise Exception("API返回内容为空")
                    
                print(f"API 返回内容: {content}")
                
                # 提取 JSON 代码块
                match = re.search(r"```json\s*(\{[\s\S]*?\})\s*```", content)
                if not match:
                    match = re.search(r"(\{[\s\S]*\})", content)
                if match:
                    json_str = match.group(1)
                    try:
                        data = json.loads(json_str)
                        if not isinstance(data, dict):
                            raise Exception(f"API 返回格式错误: {content}")
                            
                        # 兼容不同 key
                        test_cases = data.get("test_cases") or data.get("测试用例")
                        if test_cases:
                            # 如果是单个对象，转为列表
                            if isinstance(test_cases, dict):
                                test_cases = [test_cases]
                        elif ("title" in data or "标题" in data) and ("steps" in data or "步骤" in data):
                            test_cases = [data]
                        else:
                            raise Exception(f"API 返回内容中未找到测试用例字段: {content}")
                            
                        def clean_step(step):
                            # 去掉前面的数字编号（如"1. "、"2.2 "、"3、"等）
                            if isinstance(step, str):
                                return re.sub(r'^\s*\d+(\.\d+)*[\.、\s]+', '', step).strip()
                            return step
                            
                        def format_step(step):
                            if isinstance(step, dict):
                                return "；".join([f"{k}:{v}" for k, v in step.items() if v])
                            return clean_step(step)

                        result = [
                            TestCase(
                                id=str(uuid.uuid4()),
                                title=case.get("title") or case.get("标题"),
                                description=case.get("description") or case.get("描述"),
                                steps=[format_step(s) for s in (case.get("steps") or case.get("步骤") or [])],
                                expected_result=case.get("expected_result") or case.get("预期结果") or (
                                    "；".join([
                                        s.get("预期结果") for s in (case.get("steps") or case.get("步骤") or [])
                                        if isinstance(s, dict) and s.get("预期结果")
                                    ])
                                )
                            )
                            for case in test_cases
                        ]
                        
                        if not result:
                            raise Exception("生成的测试用例列表为空")
                            
                        return result
                    except Exception as e:
                        print("最终JSON解析失败：", e)
                        print("原始json字符串：", json_str)
                        raise Exception(f"解析测试用例失败: {str(e)}")
                else:
                    raise Exception("未找到JSON代码块，原始内容：" + content)
                    
        except Exception as e:
            print(f"生成测试用例时发生错误: {str(e)}")
            print("详细错误信息:")
            print(traceback.format_exc())
            raise Exception(f"生成测试用例失败: {str(e)}") 