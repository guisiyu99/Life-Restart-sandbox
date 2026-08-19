# 项目经验

> 当前项目长期有效的经验。  
> Developer / Tester / Bugfix 在任务完成后维护本文件。

---

## Harness 系统经验摘要

新项目开始时，Developer / Tester / Bugfix 需要同时参考：

- 当前项目经验：`.sdd/experience.md`
- 系统级经验：`<Harness 根目录>/memory/harness-experience.md`

---

## T-001 & T-002: 前端基础设施 + 登录页实现

**日期：** 2026-06-07

### 陷阱

1. **tsconfig.json baseUrl 弃用警告**
   - TypeScript 5.0+ 将 `baseUrl` 标记为弃用
   - 症状：`npm run type-check` 报警告但不影响功能

2. **npm 环境配置问题**
   - 沙箱环境下 npm 可能读取错误的配置文件路径
   - 症状：`ENOENT: no such file or directory, open '/Users/muxin/vibecodingclass/Muxin_workspace/package.json'`

3. **ESLint 依赖缺失**
   - eslint.config.js 使用 ESM 格式时需要额外的依赖包
   - 缺少：`globals`、`typescript-eslint`、`@eslint/js`

4. **Vite 路径别名配置**
   - tsconfig.json 中配置了 `@/*` 别名，但 Vite 不会自动识别
   - 构建时报错：`Rollup failed to resolve import "@/services/authService"`

### 经验

1. **修复 tsconfig.json 弃用警告**
   - 添加 `"ignoreDeprecations": "5.0"` 到 compilerOptions
   - 保留 `baseUrl` 和 `paths` 配置以支持路径别名

2. **处理 npm 环境问题**
   - 使用 `required_permissions: ["all"]` 运行 npm 命令
   - 或使用 `--legacy-peer-deps` 解决依赖冲突

3. **补齐 ESLint 依赖**
   ```bash
   npm install -D globals typescript-eslint @eslint/js --legacy-peer-deps
   ```

4. **同步配置 Vite 路径别名**
   ```typescript
   // vite.config.ts
   import path from 'path'
   
   export default defineConfig({
     resolve: {
       alias: {
         '@': path.resolve(__dirname, './src'),
       },
     },
   })
   ```

5. **遵循 Playful Geometric 设计规范**
   - 暖奶油底 #fef7ff
   - 2px 描边 + 硬阴影（4px 4px 0 #1E293B）
   - 紫色主按钮 #6b38d4
   - pill 形状按钮（border-radius: 9999px）
   - 浮动装饰几何形状

6. **Mock 数据严格对齐 api-contracts.md**
   - 所有字段必须是契约的子集
   - 不添加任何契约外字段
   - 响应格式统一：`{ code, message, data }`

### 避坑

1. **前端依赖安装前必须先运行 npm install**
   - 不要假设 node_modules 已存在
   - T-001 scaffolding 可能没有自动安装依赖

2. **ESLint 警告需要修复**
   - `@typescript-eslint/no-explicit-any`：不要使用 `any`，改用 `unknown` + 类型断言
   - `react-refresh/only-export-components`：组件和非组件代码要分离文件

3. **路径别名双重配置**
   - tsconfig.json 配置 `paths` 给 TypeScript 用
   - vite.config.ts 配置 `resolve.alias` 给 Vite 构建用
   - 两者必须同步，否则构建失败

4. **Mock 切换点**
   - authService 中通过 `import.meta.env.VITE_USE_MOCK` 判断
   - 前端 .env 中设置 `VITE_USE_MOCK=true/false`
   - 后端接口实现后只需修改环境变量即可切换

5. **Zustand store 初始化**
   - authStore 需要在应用启动时调用 `loadAuth()` 恢复本地状态
   - 建议在 App.tsx 或 main.tsx 中初始化

---

### Bugfix: 对局页主题选择文字看不清

- **触发**：用户验收 P05，右侧「生活圈」白字浅底、主题 chip 多数不可见
- **根因**：Vite 默认 `index.css` 的 `color-scheme: light dark` 在系统深色偏好下让原生 button 渲染浅色文字；组件未显式设置 `color`
- **已有经验回查**：无
- **修复**：清理 `index.css` 冲突规则；`theme.css` 全局 `button:not(.ant-btn) { color: var(--fg-main) }`；GamePlayPage 圈子/主题 chip 使用高对比配色
- **避坑规则**：
  1. T-001 scaffold 后必须删除或精简 Vite 默认 `index.css`（dark-mode、#root text-align:center 等）
  2. 所有原生 `<button>` 必须显式 `color: var(--fg-main)`；浅色背景 active 态用深色文字（如 `#9d174d`）
  3. 主题 chip 边框用 `--border-dark` 而非 `--border-light`，避免「空按钮」视觉
  4. Tester 验收时在浅色/深色系统偏好下各测一次可读性

### Bugfix: 圈子 Tab 与子主题按钮样式层级不清

- **触发**：用户反馈 tab 和下面按钮需做样式区分
- **根因**：`.circle-tab` 与 `.theme-chip` 复用相同矩形描边按钮形态，缺少一级/二级视觉层级
- **已有经验回查**：有（同模块文字对比度修复），但未覆盖控件层级
- **修复**：Tab 改为 pill 分段控制器 + 渐变选中；子主题改为小 chip + 虚线分隔 + 分区标签
- **避坑规则**：
  1. P05 右侧面板必须区分两级：一级「人生圈子」用 segmented tab，二级「子主题」用 compact chip grid
  2. 不得让 Tab 与子主题 chip 共用同一套 padding/圆角/边框组合
  3. 二级区域上方加 `picker-section-label` + 虚线 `border-top` 分隔

### B00: 后端基础设施

- **PYTHONPATH**：从 `backend/` 启动脚本/uvicorn 时用 `PYTHONPATH=.:..`（`.` 导入 `src`，`..` 导入 `pycore`）
- **pycore 依赖**：`loguru` 需写入 `backend/requirements.txt`
- **配置**：禁止 `os.getenv`；DotEnv loader 处理逗号分隔的 `CORS_ORIGINS`
- **SQLite**：`session.py` 中 `normalize_database_url` 解析相对路径并创建目录

### B01: 用户认证

- **分层**：`repositories/user_repo` → `services/auth_service` → `api/routes/auth`
- **密码**：只用 `bcrypt`，禁止 passlib
- **测试**：`conftest.py` 用内存 SQLite + `dependency_overrides[get_db]`，不污染业务库
- **前端**：登录/注册 401 时 axios 拦截器不要 redirect（避免密码错误刷新页面）

### B03: AI 事件抽取

- **DeepSeek**：`httpx.AsyncClient(trust_env=False)` 调用 `/v1/chat/completions`，`response_format: json_object`
- **降级**：AI 失败自动读 `backend/src/data/preset_events.json`
- **每次抽卡**：返回 1 个 event，`count` 表示本轮应完成事件数
- **规则**：age_round 1-4 需 circle+theme；5-7 仅 circle；8 全随机

### B04: 决策提交与轮次推进

- **choices**：追加 decision 到 JSON 数组，更新 money/energy/joy（energy/joy 下限 0）
- **advance-round**：age_round +1，age_range 从 `AGE_RANGES` 映射
- **响应**：choices 返回完整 GamePublic + `last_decision`（对齐前端 mock）
- **第 8 轮后**：advance-round 返回 4005「已是最后一轮」

### B05: 游戏结束与 AI 人生回顾

- **finish**：需 age_round==8；status→completed；持久化 ai_review
- **DeepSeek**：`generate_life_review` 基于 decisions + 最终属性生成 200-300 字总结
- **降级**：AI 失败返回 code=5002 + 模板总结；前端须同时接受 200 与 5002
- **outcome_tags**：joy≥8 → 平衡人生；money≥200000 → 事业达人；否则平凡之路

### B06: 历史档案查询

- **GET /api/archives**：仅返回 `status=completed` 对局，支持 page/page_size
- **GET /api/archives/{id}**：完整 decisions + ai_review + outcome_tags
- **character_name**：仅存前端 localStorage，列表/详情页用 `gameService.loadCharacterName(id)`
- **列表扩展字段**：outcome_tags、decision_count、summary（ai_review 前 40 字）

### 轮次工资累计（默认在职）

- **规则**：每轮结束后，金钱 += 本轮年薪 × 本轮年数；默认初始年薪 10 万，每进入下一轮年薪 ×1.12
- **触发点**：`advance-round` 结算刚结束轮次；第 8 轮在 `finish` 时结算（无 advance）
- **年数**：22-25→3，25-30→5，…，50-60→10，60-70→10
- **响应**：advance-round 返回 `round_salary_income`、`annual_salary`（下一轮年薪）
- **就业绑定**：`employment_status` 存库；仅 `employed` 发固定工资
  - 子主题 `创业` 或选项含创业语义 → `entrepreneur`（无工资）
  - 选项含辞职/失业/裸辞等 → `unemployed`（无工资）
  - 选项含入职/重返职场等 → 恢复 `employed`
- **前端**：角色名仍 localStorage；列表/详情用 `loadCharacterName`

### Bugfix: 选工作后仍失业、无工资累积

- **触发**：用户选「工作」主题仍提示失业，轮次结束无工资
- **根因**：失业关键词匹配了事件描述（如「裁员」「辞职」）；「工作」主题未恢复 employed
- **修复**：仅对 `chosen_option` 判失业/创业；`theme=工作` 且未离职 → employed
- **避坑**：就业状态必须反映玩家选择，不得用 event_title/description 全文扫描

---

### Bugfix: 创建角色失败（POST /api/games 404）

- **触发**：用户点击「开始人生」提示创建失败
- **根因**：uvicorn 在 B02 路由合入前启动且未带 `--reload`，旧进程无 `/api/games` 路由
- **已有经验回查**：B00 有启动命令，但未写「新增路由必须重启」
- **为什么仍然犯错**：交付 B02/B03 时未强制重启后端；404 被前端统一显示为「创建失败」
- **修复**：重启后端并启用 `--reload`；GameNewPage 对 404 给出明确提示
- **避坑规则**：
  1. 后端开发命令必须带 `--reload`：`PYTHONPATH=.:.. ../.venv/bin/python -m uvicorn src.main:app --host 127.0.0.1 --port 8099 --reload`
  2. 新增/修改路由后若未用 reload，必须手动重启 8099 进程
  3. 验收前可用 `PYTHONPATH=.:.. python -c "from src.main import app; ..."` 列出路由，或 curl `POST /api/games` 确认非 404
  4. 前端 catch 404 时应提示「后端需重启」而非泛化「创建失败」

---
