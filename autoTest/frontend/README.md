# 前端项目

使用 Vue 3 + TypeScript + Vite 构建的前端项目。

## 功能特点

- 现代化的用户界面
- 文件上传组件
- 测试用例展示
- 响应式设计

## 技术栈

- Vue 3
- TypeScript
- Vite
- Element Plus
- Axios

## 快速开始

1. 安装依赖
```bash
npm install
```

2. 启动开发服务器
```bash
npm run dev
```

3. 构建生产版本
```bash
npm run build
```

## 项目结构

```
frontend/
├── src/
│   ├── assets/           # 静态资源
│   ├── components/       # 组件
│   │   ├── FileUpload.vue    # 文件上传组件
│   │   └── TestCaseList.vue  # 测试用例列表组件
│   ├── views/            # 页面
│   │   └── Home.vue      # 主页
│   ├── router/           # 路由配置
│   ├── store/            # 状态管理
│   ├── utils/            # 工具函数
│   ├── App.vue           # 根组件
│   └── main.ts           # 入口文件
├── public/               # 公共资源
├── index.html            # HTML模板
├── package.json          # 项目配置
├── tsconfig.json         # TypeScript配置
└── vite.config.ts        # Vite配置
```

## API 调用

前端通过以下接口与后端交互：

- POST `/api/upload` - 上传文档并获取测试用例 