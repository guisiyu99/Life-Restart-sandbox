# 原型说明 — 重启人生沙盘模拟

## 来源

- **工具**：Google Stitch
- **原始目录**：`stitch_life_restart_sandbox_simulator/`（用户导出）
- **SDD 规范目录**：本目录 `docs/prototypes/`
- **设计 Token**：`design-tokens/DESIGN.md`（Neo-Sandbox Play）
- **Stitch 提示词**：项目根目录 `Stitch_prompt.md`

## 原型形态

**静态 PNG 高保真截图**（Stitch 未导出 HTML）。用于视觉对齐与 PRD/开发参考；**不可当作生产前端源码**。

浏览入口：在浏览器打开 [`index.html`](./index.html) 查看全部 8 屏平铺预览。

## 页面清单与文件映射

| SDD 页面 | 目录 | Stitch 源文件 |
|----------|------|---------------|
| P01 登录页 | `01-login/` | `_1/screen.png` |
| P02 注册页 | `02-register/` | `_3/screen.png` |
| P03 首页 | `03-home/` | `_2/screen.png` |
| P04 角色创建 | `04-character-creation/` | `_4/screen.png` |
| P05 对局主界面 | `05-game-main/` | `_5/screen.png` |
| P06 人生回顾 | `06-life-review/` | `_6/screen.png` |
| P07 历史人生档案 | `07-history-list/` | `_8/screen.png` |
| P08 历史复盘详情 | `08-history-detail/` | `_7/screen.png` |

## 关键用户路径（流程演示）

```text
P01 登录 → P03 首页 → P04 创角 → P05 对局（8 轮）→ P06 回顾 → P07 档案列表 → P08 详情
P02 注册 → P03 首页
P08 / P06 → P04 重开
```

## 组件清单（生产需实现）

- 全局顶栏 / 页脚
- Candy 主按钮、Ghost 次按钮
- Sticker 表单卡片
- 三维 Stat Chip（金钱 / 精力 / 喜悦）
- 8 轮 Timeline Stepper
- 生活圈 / 事业圈 Tab + 16 主题宫格（年龄段规则控制显隐）
- 中央 Life Event Card + 翻牌动效
- AI 总结区块（loading + 兜底模板）
- 历史 Archive Card 列表

## Mock / 真实 API 边界

| UI 区域 | MVP 数据来源 |
|---------|-------------|
| 登录 / 注册 | 真实后端 Auth API |
| 创角 / 对局状态 | 真实 Game Session API |
| 事件文案 / 选项 | **DeepSeek** 生成；失败 → 预设兜底事件 |
| 人生回顾 AI 段落 | **DeepSeek**；失败 → 模板文案 |
| 历史列表 / 详情 | 真实存档 API |

## 视觉效果 — 必须生产实现

- 2px 描边 + 硬阴影（4px offset，无 blur）
- Outfit / Plus Jakarta Sans（中文 Noto Sans SC）
- 生活圈粉 / 事业圈紫 / 金钱琥珀 / 精力绿
- P05 翻牌动画（rotateY + press 阴影）
- 点阵背景 + 低 opacity 几何装饰

## 仅原型展示、MVP 可裁剪

- P03 首页 Hero 3D 插图与底部三 feature 卡片（PRD 首页仅标题 + 两按钮）
- P04 右侧写实头像、潜能雷达图（可改为几何占位）
- P07 右侧「生涯概览 / 人生实验室」侧栏（MVP 可仅保留列表）
- P08 时间轴右侧电影感插画（MVP 可纯文字时间轴）
- P05 右下「当前场景：城市广场」地图预览（非 MVP）

## 验证报告

详见 `.sdd/tmp/prototype-validation.md`
