from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os
from dotenv import load_dotenv
import hmac
import base64
import json
import datetime
import hashlib
import websockets
import asyncio

load_dotenv()

router = APIRouter()

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

def create_url():
    # 获取当前时间戳
    now = datetime.datetime.now()
    date = now.strftime('%a, %d %b %Y %H:%M:%S GMT')
    
    # 拼接字符串
    signature_origin = f"host: spark-api.xf-yun.com\ndate: {date}\nGET /v2.1/chat HTTP/1.1"
    
    # 进行hmac-sha256进行加密
    signature_sha = hmac.new(
        os.getenv('API_SECRET').encode('utf-8'),
        signature_origin.encode('utf-8'),
        digestmod=hashlib.sha256
    ).digest()
    
    signature_sha_base64 = base64.b64encode(signature_sha).decode(encoding='utf-8')
    
    authorization_origin = f'api_key="{os.getenv("API_KEY")}", algorithm="hmac-sha256", headers="host date request-line", signature="{signature_sha_base64}"'
    
    authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')
    
    # 将请求的鉴权参数组合为字典
    v = {
        "authorization": authorization,
        "date": date,
        "host": "spark-api.xf-yun.com"
    }
    
    # 拼接鉴权参数，生成url
    url = f'wss://spark-api.xf-yun.com/v2.1/chat?authorization={v["authorization"]}&date={v["date"]}&host={v["host"]}'
    return url

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        url = create_url()
        async with websockets.connect(url) as websocket:
            # 构建请求数据
            data = {
                "header": {
                    "app_id": os.getenv('APP_ID')
                },
                "parameter": {
                    "chat": {
                        "domain": "general",
                        "temperature": 0.5,
                        "max_tokens": 2048
                    }
                },
                "payload": {
                    "message": {
                        "text": [
                            {"role": "user", "content": request.message}
                        ]
                    }
                }
            }
            
            # 发送请求
            await websocket.send(json.dumps(data))
            
            # 接收响应
            response = await websocket.recv()
            response_data = json.loads(response)
            
            # 提取回复内容
            if 'payload' in response_data and 'message' in response_data['payload']:
                content = response_data['payload']['message']['text'][0]['content']
                return ChatResponse(response=content)
            else:
                raise HTTPException(status_code=500, detail="Invalid response format")
                
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 