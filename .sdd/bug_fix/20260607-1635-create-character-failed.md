# Bug 修复报告：创建角色失败

## 用户原话

> 创建角色失败

## 经验回查

- 是否已有相关经验：部分（B00 启动说明），但未强调「新增路由后必须重启」
- 相关经验：B00 PYTHONPATH / uvicorn 启动命令
- 为什么仍然犯错：B02 游戏路由合入后，运行中的 uvicorn 未带 `--reload`，旧进程仍只暴露 auth 路由

## 问题分析

- 现象：角色创建页点击「开始人生」提示「创建失败」
- 影响范围：所有依赖 `POST /api/games` 的流程
- 直接原因：运行中后端对 `POST /api/games` 返回 HTTP 404（FastAPI `{"detail":"Not Found"}`）
- 根本原因：8099 端口上的 uvicorn 进程在 B02 路由注册之前启动，且未使用 `--reload`，未加载 `game_router`
- 涉及文件：`backend/src/main.py`（路由已正确注册）、`frontend/src/pages/GameNewPage.tsx`

## 修复方案

- 修改文件：
  - 重启后端：`uvicorn ... --reload`
  - `frontend/src/pages/GameNewPage.tsx`：404 时给出明确提示
- 修改说明：代码本身无缺陷；运维侧重启加载新路由；前端增强错误可读性

## 验证方式

- 终端验证：
  ```bash
  curl -s http://127.0.0.1:8099/health
  # 登录后
  curl -s -X POST http://127.0.0.1:8099/api/games \
    -H "Authorization: Bearer <token>" \
    -H "Content-Type: application/json" \
    -d '{"money":50000,"energy":10,"joy":0}'
  # 应返回 code=200 及 game 对象
  ```
- 前端验证：登录 → 创建角色 → 点击「开始人生」→ 跳转 `/game/{id}`

## experience.md 更新

- 新增条目：后端路由变更后必须重启或使用 `--reload`
- 后续避坑规则：Developer 交付 Bxx 后提醒用户重启；Tester 404 时先查 openapi/路由列表
