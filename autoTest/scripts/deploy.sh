#!/bin/bash

# 设置错误时退出
set -e

echo "开始部署..."

# 创建虚拟环境（如果不存在）
if [ ! -d ".venv" ]; then
    echo "创建虚拟环境..."
    python -m venv .venv
fi

# 激活虚拟环境
source .venv/bin/activate

# 安装依赖
echo "安装依赖..."
pip install -r requirements.txt

# 运行测试
echo "运行测试..."
pytest backend/tests/

# 启动服务
echo "启动服务..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

echo "部署完成！" 