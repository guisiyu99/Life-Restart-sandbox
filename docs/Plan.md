# 开发计划

> 设计阶段与开发阶段的衔接文件。所有开发进度以本文件为准。  
> 版本：V1.0  
> 日期：2026-06-07

---

## 一、功能清单总览

| 序号 | 功能名称 | 一句话描述 | 对应页面 | 优先级 | 状态 |
|------|---------|-----------|---------|--------|------|
| F01 | 用户认证 | 邮箱/密码注册登录 + JWT Token 认证 | P01, P02 | MVP | 待开发 |
| F02 | 首页与创角 | 首页入口 + 姓名与三维初始属性 | P03, P04 | MVP | 待开发 |
| F03 | 对局主流程 | 8 轮年龄段 + 圈/主题规则 + 翻牌事件 + 抉择 | P05 | MVP | 待开发 |
| F04 | AI 事件生成 | DeepSeek 生成事件；失败走预设兜底 | P05 | MVP | 待开发 |
| F05 | 人生回顾 | 规则结局 + AI 总结 + 自动归档 | P06 | MVP | 待开发 |
| F06 | 历史档案 | 列表与详情复盘 | P07, P08 | MVP | 待开发 |
| F08 | 游戏中断与恢复 | 保存进度，下次登录继续 | 全部页面 | V2+ | 待开发 |

---

## 二、数据契约摘要

> 完整数据契约见 `docs/PRD.md` 第四章「数据契约确认清单」。  
> 统一响应格式与完整接口契约见 `docs/api-contracts.md`（唯一权威源，不在本文件重复列出）。

### 核心实体

1. **User（用户）**
   - `id`, `email`, `password_hash`, `created_at`

2. **Game（游戏记录）**
   - `id`, `user_id`, `status`, `age_round`, `money`, `energy`, `joy`, `decisions`, `ai_review`, `created_at`, `updated_at`

3. **Decision（决策记录，存储在 Game.decisions JSON）**
   - `round`, `age_range`, `circle`, `theme`, `event_title`, `event_description`, `chosen_option`, `money_change`, `energy_change`, `joy_change`

### 统一响应格式

- 成功：`{ "code": 200, "message": "success", "data": {...} }`
- 错误：`{ "code": 4xxx, "message": "错误描述", "data": null }`

---

## 二点五、外部服务与测试权限清单

> **开发硬门禁**：本清单是 PRD「五、外部依赖与配置」经用户确认后的落定版，二者必须一致，且所有「状态」列不得停留在「待确认」。任一外部依赖的供应商、关键字段、Key/账号来源悬空，按 router「开发门禁」不得进入开发，只能走用户明确选择的 Mock/降级。真实 Key / Token / Secret 不写入本文档或任何 `docs/**`、`.sdd/**` 可读产物，只记录字段名、用途和配置状态；真实值只能进入 `.env` 等配置文件。

| 服务 | 用途 | 配置项字段 | MVP 必需 | Tester 完整联调权限 | 缺失时策略 | 状态 |
|------|------|------------|----------|--------------------|-----------|----|
| DeepSeek AI | 事件生成 + 人生回顾生成 | `LLM_API_KEY`, `LLM_BASE_URL`, `LLM_MODEL` | 是 | 测试 Key + 可调用额度 | 降级到预设事件库 + 模板化总结 | **已确认**<br/>Key 已提供并存储在 `backend/.env` |

**说明：**
- DeepSeek API Key 由用户提供，已存储在 `backend/.env`
- Base URL: `https://api.deepseek.com/v1`
- Model: `deepseek-chat`
- 降级策略：AI 调用失败时，事件生成使用预设事件库（每个子主题预存 20 个事件），人生回顾使用模板化总结

---

## 三、前端开发清单

### 前端技术选型

| 层级 | 默认选择 | 说明 |
|------|----------|------|
| 框架 | React 18 | 业务型 Web App 默认前端框架 |
| 语言 | TypeScript | 所有组件、service、DTO 必须类型化 |
| 构建工具 | Vite 5 | 本地开发、代理、构建统一使用 Vite |
| 路由 | react-router-dom 6 | 页面路由与鉴权守卫 |
| 状态管理 | Zustand | 登录态、游戏状态、全局 UI 状态 |
| 请求库 | Axios | 统一 API 实例、拦截器、错误处理 |
| 移动端 H5 组件库 | Ant Design Mobile | 手机浏览器、微信内网页、PWA |
| 工程化 | ESLint + Prettier + type-check + build | 自动验收必须覆盖 |
| 动画 | CSS3 Transitions + React Transition Group | 卡片翻转、页面过渡 |

### 前端页面清单

| 序号 | 页面名称 | 路由 | 涉及功能 | Mock 数据来源 | 原型文件 | 状态 |
|------|---------|------|---------|--------------|----------|------|
| P01 | 登录页 | `/login` | F01 | POST /api/auth/login | `docs/prototypes/01-login` | 待开发 |
| P02 | 注册页 | `/register` | F01 | POST /api/auth/register | `docs/prototypes/02-register` | 待开发 |
| P03 | 首页 | `/` | F02 | — | `docs/prototypes/03-home` | 待开发 |
| P04 | 角色创建 | `/game/new` | F02 | POST /api/games | `docs/prototypes/04-character-creation` | 待开发 |
| P05 | 对局主界面 | `/game/:id` | F03, F04 | draw-event, choices, advance | `docs/prototypes/05-game-main` | 待开发 |
| P06 | 人生回顾 | `/game/:id/review` | F05 | POST /api/games/:id/finish | `docs/prototypes/06-life-review` | 待开发 |
| P07 | 历史档案 | `/archives` | F06 | GET /api/archives | `docs/prototypes/07-history-list` | 待开发 |
| P08 | 历史详情 | `/archives/:id` | F06 | GET /api/archives/:id | `docs/prototypes/08-history-detail` | 待开发 |

### 前端核心组件

| 组件名称 | 文件路径 | 功能 | 依赖 |
|---------|---------|------|------|
| AuthGuard | `src/components/AuthGuard.tsx` | 路由鉴权守卫 | authStore |
| GameCard | `src/components/GameCard.tsx` | 卡片翻转组件（事件卡片） | CSS3 Transitions |
| AttributeBar | `src/components/AttributeBar.tsx` | 三大属性展示条 | - |
| ThemeSelector | `src/components/ThemeSelector.tsx` | 圈和子主题选择器 | - |
| DecisionHistory | `src/components/DecisionHistory.tsx` | 决策轨迹时间线 | - |

### 前端自动验收标准

- [ ] 所有页面 UI 与原型文件（`docs/prototypes/index.html`）一致
- [ ] 所有页面使用 Mock 数据可正常交互
- [ ] Mock 数据格式与 `api-contracts.md` 完全一致
- [ ] `npm run type-check` 通过
- [ ] `npm run lint` 通过
- [ ] **Agent/Tester 自动验收通过**

> 前端 Mock 页面完成后触发用户门禁，由用户验收 UI/UX 效果；用户确认后自动进入后端基础设施开发。  
> 前端 Mock 只用于前端 MVP 和接口契约对齐；后端业务任务完成时，必须把对应前端 service/page 切到 `VITE_USE_MOCK=false` 的真实后端联调路径。

---

## 四、后端开发清单

### 后端技术选型

| 层级 | 选择 | 说明 |
|------|------|------|
| 框架 | FastAPI + pycore | pycore 提供配置、日志、数据库、API 服务器基础设施 |
| 语言 | Python 3.11+ | 类型提示、异步支持 |
| ORM | SQLAlchemy 2.0 | 异步 ORM，支持 SQLite/PostgreSQL |
| 数据库 | SQLite | MVP 阶段单机部署；V2+ 迁移 PostgreSQL |
| 认证 | JWT (python-jose) | 无状态 Token 认证 |
| 密码加密 | BCrypt (passlib) | 安全哈希算法 |
| HTTP 客户端 | httpx | 调用 DeepSeek API（trust_env=False） |
| 工程化 | ruff + mypy + pytest | 代码质量门禁 |

### 后端任务清单

| 序号 | 功能名称 | 依赖 | 对应接口 | 状态 |
|------|---------|------|---------|------|
| B00 | 基础设施 | pycore 框架 | GET /health | 待开发 |
| B01 | 用户认证模块 | B00 | POST /api/auth/register, POST /api/auth/login, GET /api/auth/me | 待开发 |
| B02 | 游戏创建与查询 | B00, B01 | POST /api/games, GET /api/games/:id | 待开发 |
| B03 | 事件抽取模块 | B00, B02, DeepSeek AI | POST /api/games/:id/draw-event | 待开发 |
| B04 | 决策提交与属性更新 | B00, B02 | POST /api/games/:id/choices | 待开发 |
| B05 | 年龄段推进 | B00, B02 | POST /api/games/:id/advance-round | 待开发 |
| B06 | 游戏结束与 AI 回顾 | B00, B02, DeepSeek AI | POST /api/games/:id/finish | 待开发 |
| B07 | 归档查询 | B00, B01 | GET /api/archives, GET /api/archives/:id | 待开发 |

### 后端模块结构

```
backend/
├── src/
│   ├── main.py                 # FastAPI 应用入口（基于 pycore.api.APIServer）
│   ├── api/
│   │   ├── routes/
│   │   │   ├── auth.py         # 认证路由（注册、登录、获取用户信息）
│   │   │   ├── game.py         # 游戏路由（创建、查询、抽取事件、提交决策、推进轮次、完成游戏）
│   │   │   └── archive.py      # 归档路由（查询历史游戏）
│   │   └── deps.py             # 依赖注入（get_current_user, get_db）
│   ├── services/
│   │   ├── user_service.py     # 用户业务逻辑
│   │   ├── game_service.py     # 游戏业务逻辑
│   │   ├── event_service.py    # 事件生成服务（AI + 预设事件库）
│   │   └── ai_service.py       # DeepSeek AI 调用服务
│   ├── repositories/
│   │   ├── user_repo.py        # 用户数据访问层
│   │   └── game_repo.py        # 游戏数据访问层
│   ├── db/
│   │   ├── models.py           # SQLAlchemy 模型（User, Game）
│   │   └── session.py          # 数据库会话管理（基于 pycore/integrations/db/）
│   ├── core/
│   │   └── config.py           # 配置管理（基于 pycore.core.ConfigManager）
│   └── data/
│       └── preset_events.json  # 预设事件库（降级方案）
├── tests/
│   ├── test_auth.py            # 认证模块测试
│   ├── test_game.py            # 游戏模块测试
│   └── test_ai_service.py      # AI 服务测试
├── scripts/
│   └── init_db.py              # 数据库初始化脚本
├── .env                        # 环境变量配置（包含 LLM_API_KEY）
└── requirements.txt            # Python 依赖
```

### 后端任务验收规则

- **基础设施任务基于 pycore 框架**：禁止自己重写 config.py、server.py、logger.py；配置管理使用 `pycore.core.ConfigManager`，服务器使用 `pycore.api.APIServer`，数据库骨架从 `pycore/integrations/db/` 复制模板
- 基础设施任务由 Agent 自动连续执行，不触发用户门禁；验收标准：ruff/mypy 通过、单元测试通过、`GET /health` 返回 200
- 对应前端页面或 service 的业务任务：必须在任务内完成真实联调验收，每个功能是一个完整闭环（后端 API + 前端 Mock 切真实）
- 真实联调验收至少包含：
  - `VITE_USE_MOCK=false` 时前端调用真实后端 API
  - 对应页面核心操作可用
  - 页面不得展示该功能相关 `[Mock]` 数据、Mock 账号提示或 Mock-only 文案
  - Tester 能证明请求命中真实后端，而不是 `frontend/src/mocks/*`
- 最终 E2E / 回归阶段只做全系统复查，不承担第一次前后端联调
- 涉及外部服务的后端任务，必须引用「外部服务与测试权限清单」；如果必要 Key / 权限缺失，只能标记 Mock/fallback 验收，不得宣称真实外部服务联调通过

---

## 五、开发顺序建议

> 以下顺序是默认推荐节奏，实际开发以 Planner 产出的 `.sdd/tasks.json` 为准。

### 阶段 1：前端 MVP（Mock，用户先验收 UI/UX）

**目标：**完成全部 8 个页面的 UI 和 Mock 交互，用户确认视觉效果和用户体验。

**任务顺序：**
1. **前端脚手架搭建**
   - 初始化 Vite + React + TypeScript 项目
   - 配置 react-router-dom 路由
   - 配置 Zustand 状态管理
   - 配置 Axios 实例和拦截器
   - 配置 ESLint + Prettier

2. **P01 登录页（Mock）**
   - 实现登录/注册表单
   - Mock API: POST /api/auth/login, POST /api/auth/register
   - 存储 Token 到 localStorage
   - 路由守卫：未登录跳转到登录页

3. **P02 游戏配置页（Mock）**
   - 实现"开始新游戏"按钮
   - Mock API: POST /api/games
   - 跳转到年龄段选择页

4. **P03 年龄段选择页（Mock）**
   - 展示当前年龄段和三大属性
   - Mock API: GET /api/games/:id
   - 进入主题选择页

5. **P04 主题选择页（Mock）**
   - 根据年龄段显示不同选择方式（圈+主题 / 仅圈 / 自动抽取）
   - Mock API: POST /api/games/:id/draw-event
   - 跳转到事件抽取页

6. **P05 事件抽取页（Mock）**
   - 实现卡片翻转动画（CSS3 + React Transition Group）
   - 展示事件详情和选项
   - Mock API: POST /api/games/:id/choices
   - 跳转到决策结果页

7. **P06 决策结果页（Mock）**
   - 展示属性变化动画
   - "继续"按钮：本轮还有事件 → P05；本轮结束 → P03 或 P07
   - Mock API: GET /api/games/:id

8. **P07 生活回顾页（Mock）**
   - 展示 AI 生成的人生总结
   - Mock API: POST /api/games/:id/finish
   - "查看历史记录"按钮 → P08

9. **P08 历史记录详情页（Mock）**
   - 展示已完成游戏列表
   - 点击查看完整决策轨迹
   - Mock API: GET /api/archives, GET /api/archives/:id

**验收标准：**
- [ ] 所有页面 UI 与 `docs/prototypes/index.html` 完全一致
- [ ] 使用 Mock 数据可完整走通游戏流程
- [ ] `npm run type-check` 和 `npm run lint` 通过
- [ ] **用户门禁验收：用户打开页面，确认布局、配色、交互与原型一致**

---

### 阶段 2：后端基础设施（自动连续执行，不触发用户门禁）

**目标：**搭建后端基础设施，确保框架合规和服务健康。

**任务顺序：**
1. **B00 基础设施**
   - 基于 pycore 框架初始化项目结构
   - 配置 `backend/src/main.py`（使用 `pycore.api.APIServer`）
   - 配置 `backend/src/core/config.py`（使用 `pycore.core.ConfigManager`）
   - 配置 `backend/src/db/models.py`（基于 `pycore/integrations/db/models.py` 模板）
   - 配置 `backend/src/db/session.py`（基于 `pycore/integrations/db/session.py` 模板）
   - 配置 `backend/.env`（包含 LLM_API_KEY 等）
   - 实现 `GET /health` 接口
   - 编写 `backend/scripts/init_db.py` 初始化数据库

**验收标准：**
- [ ] `python -m ruff check backend/src backend/tests` 通过
- [ ] `python -m mypy backend/src backend/tests` 通过
- [ ] `python -m pytest backend/tests` 通过
- [ ] `GET /health` 返回 200
- [ ] pycore 合规检查全部通过

---

### 阶段 3：逐功能闭环开发（每个功能完成后触发用户门禁）

**目标：**按业务依赖逐个推进功能，每个功能 = 后端真实 API + 前端 Mock 切真实 + 联调验收。

**任务顺序：**
1. **B01 用户认证模块 + 前端联调**
   - 后端实现：POST /api/auth/register, POST /api/auth/login, GET /api/auth/me
   - 前端切换：`frontend/src/services/auth.ts` 从 Mock 切到真实 API
   - 验收：前端登录页可注册/登录，Token 有效

2. **B02 游戏创建与查询 + 前端联调**
   - 后端实现：POST /api/games, GET /api/games/:id
   - 前端切换：`frontend/src/services/game.ts` 对应接口切到真实 API
   - 验收：P02 创建游戏，P03 查看游戏状态

3. **B03 事件抽取模块 + 前端联调**
   - 后端实现：POST /api/games/:id/draw-event（调用 DeepSeek AI + 降级预设事件库）
   - 前端切换：`frontend/src/services/game.ts` 事件抽取切到真实 API
   - 验收：P04 选择主题，P05 翻卡片显示真实 AI 生成的事件

4. **B04 决策提交与属性更新 + 前端联调**
   - 后端实现：POST /api/games/:id/choices
   - 前端切换：`frontend/src/services/game.ts` 决策提交切到真实 API
   - 验收：P05 选择选项，P06 展示属性变化

5. **B05 年龄段推进 + 前端联调**
   - 后端实现：POST /api/games/:id/advance-round
   - 前端切换：`frontend/src/services/game.ts` 推进轮次切到真实 API
   - 验收：P06 进入下一年龄段，P03 更新年龄段显示

6. **B06 游戏结束与 AI 回顾 + 前端联调**
   - 后端实现：POST /api/games/:id/finish（调用 DeepSeek AI 生成人生总结）
   - 前端切换：`frontend/src/services/game.ts` 完成游戏切到真实 API
   - 验收：P07 展示真实 AI 生成的人生回顾

7. **B07 归档查询 + 前端联调**
   - 后端实现：GET /api/archives, GET /api/archives/:id
   - 前端切换：`frontend/src/services/archive.ts` 切到真实 API
   - 验收：P08 查看历史游戏列表和详情

**每个功能验收标准：**
- [ ] 后端 ruff/mypy/pytest 全部通过
- [ ] 前端对应 service 已切到真实 API（`VITE_USE_MOCK=false`）
- [ ] 前端页面核心操作可用，不展示 `[Mock]` 标识
- [ ] Tester 验证请求命中真实后端
- [ ] **用户门禁验收：用户从前端页面操作验证功能可用**

---

### 阶段 4：E2E 回归测试

**目标：**完整流程走通，无阻塞性 Bug。

**验收标准：**
- [ ] 用户可完整走通：注册 → 登录 → 创建游戏 → 完成 8 轮 → 查看 AI 回顾 → 查看历史记录
- [ ] 所有页面 UI 与原型一致
- [ ] 所有接口符合 `api-contracts.md`
- [ ] DeepSeek AI 调用成功，降级方案可用
- [ ] **用户门禁验收：全流程通过，无阻塞性 Bug**

---

## 六、端口约定

> 端口权威源见 `harness-core/protocols/development-rules.md`「端口约定」。

| 环境 | 前端端口 | 后端端口 | 说明 |
|------|---------|---------|------|
| Agent/Tester 自动验证 | 5199 | 8099 | 开发阶段默认端口 |
| 用户门禁验收 | 5175 | 8003 | 用户验收时启动端口 |

### Vite 代理配置

**前端配置：**`frontend/vite.config.ts`

```typescript
export default defineConfig({
  server: {
    port: 5199, // 开发阶段默认端口
    proxy: {
      '/api': {
        target: process.env.VITE_BACKEND_PROXY_TARGET || 'http://localhost:8099',
        changeOrigin: true,
      },
    },
  },
});
```

**环境变量：**`frontend/.env`

```
VITE_API_BASE_URL=/api
VITE_USE_MOCK=true  # 前端 Mock 阶段设为 true，后端联调时设为 false
```

**用户门禁验收时：**

```bash
# 前端
VITE_BACKEND_PROXY_TARGET=http://localhost:8003 npm run dev -- --port 5175

# 后端
cd backend && uvicorn src.main:app --host 127.0.0.1 --port 8003
```

**CORS 配置：**后端 CORS 同时允许 `localhost/127.0.0.1` 的 `5199` 与 `5175`

---

## 七、风险与缓解

| 风险 | 影响 | 概率 | 缓解策略 |
|------|------|------|---------|
| DeepSeek API 限流/故障 | 事件生成失败，游戏体验下降 | 中 | 降级到预设事件库（每个子主题 20 个事件） |
| SQLite 并发限制 | 多用户同时操作可能阻塞 | 低 | MVP 阶段单用户演示可接受；V2 迁移 PostgreSQL |
| 前端包体积过大 | 首屏加载慢 | 中 | 代码分割 + 懒加载路由 |
| AI 生成内容不可控 | 可能生成不合适内容 | 低 | 提示词约束 + 内容过滤关键词 |
| 游戏平衡性调优 | 属性变化幅度可能影响体验 | 中 | 收集用户反馈，迭代调整数值 |

---

## 八、质量门禁

### 前端质量门禁

- `npm run type-check`：TypeScript 类型检查
- `npm run lint`：ESLint 代码风格检查
- 原型文案/样式核对：所有页面与 `docs/prototypes/index.html` 一致
- Mock 字段对齐：所有 Mock 数据是 `api-contracts.md` 的子集

### 后端质量门禁

- `python -m ruff check backend/src backend/tests`：代码风格检查
- `python -m mypy backend/src backend/tests`：类型检查
- `python -m pytest backend/tests`：单元测试
- pycore 合规检查：不重写框架组件，使用 ConfigManager/APIServer/模板
- 数据库隔离：测试库与业务库分离，测试清理不影响真实数据

### 通用门禁

- 代码符合 rules 文件规范
- 接口与 `api-contracts.md` 一致
- 敏感值（API Key）仅存在于 `.env`，不泄露到文档或日志
- Vite 代理配置正确，前端不硬编码后端 URL

---

## 九、开发注意事项

### 前端开发注意事项

1. **严格对齐原型文件**：所有文案、布局、配色、间距、圆角、字体大小必须与 `docs/prototypes/index.html` 完全一致
2. **Mock 数据规范**：
   - 字段必须是 `api-contracts.md` 的子集
   - 每个 endpoint 独立 DTO，不直接返回内部实体
   - 同一功能域的全部 endpoint 一起核对
3. **卡片翻转动画**：使用 CSS3 `transform: rotateY()` + React Transition Group
4. **路由守卫**：未登录用户自动跳转到登录页
5. **响应式设计**：移动端优先，适配 375px-768px 屏幕宽度

### 后端开发注意事项

1. **pycore 框架合规**：
   - 不重写 config.py、server.py、logger.py
   - 使用 `pycore.core.ConfigManager` 读取配置
   - 使用 `pycore.api.APIServer` 创建应用
   - 数据库模板从 `pycore/integrations/db/` 复制扩展
2. **DeepSeek AI 调用**：
   - 使用 `httpx.AsyncClient(trust_env=False)` 调用 API
   - 禁止使用 SDK（如 `dashscope`）
   - 先真实调用并打印响应，再写解析逻辑
   - 设置降级方案（预设事件库）
3. **数据库路径**：
   - SQLite 路径解析为绝对路径：`backend/data/life_restart.db`
   - 创建父目录：`os.makedirs(os.path.dirname(db_path), exist_ok=True)`
4. **认证鉴权**：
   - 路由级依赖注入（`Depends(get_current_user)`）
   - 不注册全局认证中间件
5. **测试数据库隔离**：
   - 测试使用独立测试库或事务回滚夹具
   - 禁止 `drop_all` 或清空真实业务库

---

## 十、变更记录

| 版本 | 日期 | 变更内容 | 变更人 |
|------|------|---------|--------|
| V1.0 | 2026-06-07 | 初始版本，完成 Phase C 开发计划 | AI Assistant |

---

**开发计划状态：已确认，可进入开发阶段**
