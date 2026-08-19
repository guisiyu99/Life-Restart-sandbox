# Life-Restart-sandbox

AI-native life choice simulator / 人生选择模拟器 Web MVP

本项目由 SDD V7.1 管理。

## 核心目录

- `.sdd/`：项目状态、任务、经验、日志、测试报告
- `docs/`：PRD、API 契约、开发计划、原型
- `frontend/`：React + Vite 前端
- `backend/`：FastAPI 后端
- `AGENTS.md`：项目轻入口

## 环境配置

敏感配置（**勿提交 Git**）请复制示例文件后本地填写：

```bash
cp backend/.env.example backend/.env
# 编辑 backend/.env，填入 LLM_API_KEY、JWT_SECRET 等
```

`backend/.env`、`frontend/.env` 已在 `.gitignore` 中排除。
