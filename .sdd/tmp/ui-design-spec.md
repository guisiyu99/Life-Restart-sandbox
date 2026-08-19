# Design Spec

> visual_research_status: ready  
> 设计方向来源：阶段 R 选定 B+C 融合 + 用户 Stitch 导出「Neo-Sandbox Play」设计系统  
> prototype_source: Stitch（PNG 高保真静态原型，非生产 HTML）

## 界面清单（MVP）

| 界面 | 类型 | 目标视口 | 一句话用途 | 原型路径 |
|------|------|----------|-----------|----------|
| P01 登录页 | 表单页 | 桌面 1440×900 | 邮箱密码登录 | `docs/prototypes/01-login/screen.png` |
| P02 注册页 | 表单页 | 桌面 1440×900 | 邮箱注册 | `docs/prototypes/02-register/screen.png` |
| P03 首页 | 引导页 | 桌面 1440×900 | 标题 + 创建角色 / 历史档案 | `docs/prototypes/03-home/screen.png` |
| P04 角色创建 | 表单页 | 桌面 1440×900 | 姓名 + 三维初始属性 | `docs/prototypes/04-character-creation/screen.png` |
| P05 对局主界面 | 游戏页 | 桌面 1440×900 | 时间轴 + 事件卡 + 圈/主题选择 | `docs/prototypes/05-game-main/screen.png` |
| P06 人生回顾 | 详情页 | 桌面 1440×900 | 结局 + AI 总结 + 时间轴 | `docs/prototypes/06-life-review/screen.png` |
| P07 历史人生档案 | 列表页 | 桌面 1440×900 | 已完成对局列表 | `docs/prototypes/07-history-list/screen.png` |
| P08 历史复盘详情 | 详情页 | 桌面 1440×900 | 只读回顾 + 基于此重开 | `docs/prototypes/08-history-detail/screen.png` |

## 设计方向

- **选定方向**：Playful Geometric / Neo-Brutalism —「Stable Grid, Wild Decoration」
- **视觉特征**：暖奶油底、2px 粗描边、硬阴影（4px 无 blur）、Outfit 标题 + Plus Jakarta Sans 正文；生活圈粉、事业圈紫、金钱琥珀、精力翠绿
- **参考来源**：`.sdd/tmp/visual-research.md` + `docs/prototypes/design-tokens/DESIGN.md`

## 核心资产

- **Logo**：无独立 Logo 文件；标题文字「重启人生沙盘模拟」作品牌字标
- **Stitch 原型截图**：`docs/prototypes/01-login/` … `08-history-detail/`
- **设计 Token 源文件**：`docs/prototypes/design-tokens/DESIGN.md`（Stitch Neo-Sandbox Play 导出）
- **Stitch 原始目录（保留）**：`stitch_life_restart_sandbox_simulator/`、`docs/prototypes/stitch-source/`

## 视觉规格

### 色板（来自 DESIGN.md）

| Token | 值 | 用途 |
|-------|-----|------|
| background | `#fef7ff` | 页面底 |
| on-surface | `#1d1a23` | 主文字 |
| primary | `#6b38d4` | 事业圈、主 CTA |
| secondary | `#a43073` / `#fc79bd` | 生活圈、强调 |
| tertiary | `#765700` / `#f9bd22` | 金钱 |
| quaternary | `#34D399`（规范映射） | 精力 |
| border | `#7b7486` / `#E2E8F0` | 描边 |
| error | `#ba1a1a` | 表单错误 |

### 字型

- **Display / Headings**：Outfit 700–800；中文回退 Noto Sans SC Bold
- **Body / Label**：Plus Jakarta Sans 400–700
- **Scale**：display-lg 48px → label-sm 12px（见 DESIGN.md typography）

### 间距 · 圆角 · 阴影

- 间距基准 4px；md 16px 内边距；lg 24px 区块间距
- 圆角：sm 8px、md 16px、full pill
- **硬阴影**：`4px 4px 0 #1E293B`；hover `6px 6px`；active `2px 2px`
- 边框：交互元素默认 **2px solid**

### 信息密度

- 对局页（P05）：**中等偏高** — 三栏常显
- 其余页面：**克制型**，居中卡片或单列

## 组件与页面结构

### 全局

- 顶栏：产品名（左）+ 用户信息/属性 chips（右，对局页必显）
- 页脚：© 文案 + 用户协议 / 隐私政策
- 背景：点阵 grid + 浮动几何装饰（低 opacity）

### 逐页主区域

| 页面 | 主区域 |
|------|--------|
| P01 | 居中 sticker 卡片：邮箱、密码、登录、注册链接 |
| P02 | 居中卡片：邮箱、密码、确认密码、注册并登录 |
| P03 | Hero 标题 + 副标题 + 两主按钮；**原型含额外 feature 三卡片与插图（见验证偏差）** |
| P04 | 左：姓名 + 三维 stepper；右：头像/雷达装饰；底：返回 / 开始人生 |
| P05 | 左：8 轮时间轴；中：事件大卡 + A/B/C 选项；右：生活/事业 Tab + 8 主题宫格 |
| P06 | 结局标签 + 三维终局 + AI 总结卡 + 关键决策列表 + 返回首页 |
| P07 | 左：档案卡片列表；右：生涯概览侧栏（**原型扩展，MVP 可简化**） |
| P08 | 左：AI 总结 + 标签；右：属性条 + 重开/返回；下：生命轨迹时间轴 |

### 关键组件清单

- **Candy Button**：primary 紫底白字、2px 描边、硬阴影、pill 形
- **Sticker Card**：白底、16px 圆角、2px 描边、硬阴影
- **Stat Chip**：金钱/精力/喜悦 图标 + 数值
- **Life Event Card**：中央事件区；标签 pills（圈 + 主题）
- **Theme Grid**：4×2 子主题按钮；选中态 secondary 填充
- **Timeline Stepper**：8 年龄段竖向步骤
- **Archive Card**：头像 + 姓名 + 结局 tag + 三维摘要 + 日期

## 签名细节（120% 质感锚点）

- **P05 中央事件卡**：2px 描边 + 硬阴影 + 选项行内属性变化色标（+金钱/-精力）— 全产品视觉焦点

## 设计禁区

- 不照搬人生重开模拟器黑底极简全套
- 不使用无依据紫粉渐变 hero
- 不用 emoji 代替 Lucide 图标
- 不复制 Stitch 示例中的虚构人物照片作为生产素材（可换插画或几何占位）

## 气质关键词

- 友好 · 可触 · 弹跃 · 几何 · 沙盘感

## 生产前端交接要点

1. Stitch 产出为 **PNG 静态原型**，生产实现使用 **React + TypeScript + Vite + Ant Design**，视觉按本 spec 与 DESIGN.md token 定制主题
2. P05 需实现 **翻牌动画**（方案 C）：逻辑为双圈抽事件，动画为 rotateY + 硬阴影位移
3. 三维属性生产口径：**金钱（默认 50000）、精力（默认 10）、喜悦（默认 0）** — P08 原型若出现四维（智力/健康等）以 PRD 三维为准
4. DeepSeek 生成事件与回顾 — UI 需 loading / 骨架屏 / 兜底事件态
