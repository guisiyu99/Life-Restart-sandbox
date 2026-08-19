# Bug 修复报告：对局页主题选择文字看不清

## 用户原话

> /sdd-bugfix 文字显示看不清

（附截图：P05 对局页右侧「选择事件主题」面板，生活圈按钮白字浅粉底、多数主题 chip 文字不可见）

## 经验回查

- 是否存在相关历史经验：**否**
- 相关条目：无
- 为什么仍然犯错：N/A（首次出现）

## 问题分析

- **现象**：右侧主题面板中「生活圈」白字配浅粉底对比度极低；8 个主题 chip 除已选「父母」外其余看似空白；说明文字偏灰难读
- **影响范围**：P05 对局页主题选择区；同类原生 `<button>` 在其他页面也可能受影响
- **直接原因**：原生 `button`（`.circle-tab`、`.theme-chip`）未显式设置 `color`；未选中 chip 使用 `#e2e8f0` 浅边框，文字继承系统/父级浅色
- **根本原因**：Vite 脚手架遗留的 `index.css` 含 `color-scheme: light dark` 与 `@media (prefers-color-scheme: dark)`，在 macOS 深色偏好下浏览器对原生控件应用浅色文字，与白色/浅色按钮背景叠加导致不可读

## 修复方案

- **修改文件**：
  - `frontend/src/index.css` — 移除 Vite 默认 dark-mode / color-scheme 规则，仅保留 `#root` 布局
  - `frontend/src/styles/theme.css` — 全局 `button:not(.ant-btn)` 显式 `color: var(--fg-main)`；标题加主文字色
  - `frontend/src/pages/GamePlayPage.css` — 圈子 tab / 主题 chip / 提示文案对比度强化
  - `frontend/src/pages/GamePlayPage.tsx` — 底部提示改用 CSS 类
  - `frontend/src/components/AppLayout.css` — 退出按钮显式文字色

- **修改说明**：
  - 选中态圈子 tab 使用深粉 `#9d174d` / 深紫 `#5b21b6` 文字
  - 主题 chip 边框改为 `--border-dark`，未选中显式 `--fg-main` 文字
  - 提示区改用 `--fg-main` + 浅紫底 `#faf8ff`

## 验证方式

- **前端验证**：
  1. 刷新 http://localhost:5199/
  2. 登录 → 创建/进入对局 → 查看右侧主题面板
  3. 确认「生活圈/事业圈」、8 个主题名称、底部说明文字均清晰可读
  4. 切换选中主题，确认紫色选中态白字仍清晰

- **终端验证**：
  ```bash
  cd frontend && npm run type-check && npm run lint
  ```

## experience.md 更新

- 新增条目：Bugfix 文字对比度 / index.css 与 theme.css 冲突
- 后续避坑：Scaffold 后必须清理 Vite 默认 index.css；原生 button 必须显式 color
