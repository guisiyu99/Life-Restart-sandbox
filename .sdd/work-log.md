# 工作日志

> 由 Orchestrator 维护。记录项目开发、测试、修复和 blocked 状态。

---

## 2026-06-07 — B03 AI 事件抽取

- POST /api/games/{id}/draw-event：DeepSeek 优先生成，失败降级 preset_events.json
- pytest 17/17 通过
- 当前门禁：**B03** 用户验收抽卡

---

- POST /api/games、GET /api/games/{id} 已实现
- 角色姓名仍存前端 localStorage；初始属性由请求体传入
- pytest 13/13 通过
- 抽卡需等 **B03**（DeepSeek）

---

- 实现 POST /api/auth/register、login、GET /me（JWT + bcrypt）
- 前端 `VITE_USE_MOCK=false`，auth 走真实后端
- pytest 8/8 通过；curl 联调验证通过
- 当前门禁：**B01** 用户验收登录/注册

---

- PyCore + FastAPI 脚手架：`backend/src/main.py`、ConfigManager、User/Game ORM、JWT deps 骨架
- `GET /health`、`GET /api/auth/me`（无 Token 返回 401/4002）
- ruff / mypy / pytest 5 项全通过
- 启动：`cd backend && PYTHONPATH=.:.. ../.venv/bin/python -m uvicorn src.main:app --host 127.0.0.1 --port 8099`
- 下一步：**B01** 注册/登录/当前用户 + 前端 `VITE_USE_MOCK=false` 联调

---

- 8 页 Mock 全部实现：登录/注册/首页/创角/对局/回顾/档案列表/档案详情
- `npm run type-check` / `lint` / `build` 通过
- 当前门禁：**T-010** 用户验收 Mock UI
- 下一步：B00 后端基础设施

---

- 用户导出目录 `stitch_life_restart_sandbox_simulator`（8 屏 PNG + Neo-Sandbox Play DESIGN.md）
- 已整理至 `docs/prototypes/01-login` … `08-history-detail`
- 已生成 `.sdd/tmp/ui-design-spec.md`、`.sdd/tmp/prototype-validation.md`
- 已生成 `docs/prototypes/index.html` 平铺预览
- 阶段：B2 原型已导入，待用户确认验证报告
- 待办：补全 `docs/PRD.md`（阶段 A）→ 阶段 C

---

