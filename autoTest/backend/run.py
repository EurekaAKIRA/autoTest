import os
import sys
import uvicorn

# 添加项目根目录到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

if __name__ == '__main__':
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",  # 使用localhost而不是0.0.0.0
        port=8000,         # 改用8000端口
        reload=True,
        log_level="debug",  # 设置为debug级别以获取更多日志
        access_log=True,    # 启用访问日志
        proxy_headers=True, # 启用代理头
        forwarded_allow_ips="*"  # 允许所有转发IP
    ) 