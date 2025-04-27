# 测试用例生成系统

基于大模型的测试用例自动生成系统，可以根据需求文档自动生成测试用例。

## 功能特点

- 支持Word和PDF格式的需求文档上传
- 使用大模型自动生成测试用例
- RESTful API接口
- 现代化的用户界面
- 完整的测试覆盖

## 技术栈

### 后端
- FastAPI
- OpenAI API
- python-docx, pypdf
- pytest

### 前端
- Vue 3
- TypeScript
- Vite
- Element Plus
- Axios

## 快速开始

### 后端

1. 克隆项目
```bash
git clone [项目地址]
cd autoTest
```

2. 创建虚拟环境
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows
```

3. 安装依赖
```bash
pip install -r requirements.txt
```

4. 配置环境变量
创建 `.env` 文件并添加：
```
OPENAI_API_KEY=你的OpenAI API密钥
```

5. 启动服务
```bash
uvicorn backend.app.main:app --reload
```

### 前端

1. 进入前端目录
```bash
cd frontend
```

2. 安装依赖
```bash
npm install
```

3. 启动开发服务器
```bash
npm run dev
```

## 项目结构

```
PythonProject3/
│
├── .venv/                            # 虚拟环境
│
├── backend/                          # 后端主程序
│   ├── app/                          
│   │   ├── api/                      # API接口
│   │   ├── core/                     # 核心功能
│   │   ├── models/                   # 数据模型
│   │   ├── services/                 # 业务逻辑
│   │   ├── utils/                    # 工具函数
│   │   └── main.py                   # 入口文件
│   └── tests/                        # 测试文件
│
├── frontend/                         # 前端项目
│   ├── src/
│   │   ├── assets/                   # 静态资源
│   │   ├── components/               # 组件
│   │   ├── views/                    # 页面
│   │   ├── router/                   # 路由
│   │   ├── store/                    # 状态管理
│   │   ├── utils/                    # 工具函数
│   │   ├── App.vue                   # 根组件
│   │   └── main.ts                   # 入口文件
│   ├── public/                       # 公共资源
│   └── package.json                  # 项目配置
│
├── docs/                             # 项目文档
│   └── api_spec.md                   # API规范
│
├── scripts/                          # 部署脚本
│   └── deploy.sh                     # 部署脚本
│
├── requirements.txt                  # 后端依赖
└── README.md                         # 项目说明
```

## API文档

访问 `http://localhost:8000/docs` 查看完整的API文档。

## 测试

### 后端测试
```bash
cd backend
pytest
```

### 前端测试
```bash
cd frontend
npm run test
```

## 贡献指南

1. Fork 项目
2. 创建特性分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 许可证

MIT 