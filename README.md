# 重启人生沙盘模拟 · Life Restart Sandbox

> 从 22 岁到 70 岁，用一次次选择，拼出属于你的人生版本。

一款 **AI 驱动的人生决策模拟 Web 游戏**。你创建角色、经历 8 个人生阶段，在「生活圈」与「事业圈」之间做选择，翻牌遭遇随机事件，最终获得 AI 撰写的人生回顾。单局约 **15–20 分钟**。

---

## 这是什么？

**重启人生沙盘模拟** 不是传统意义上的「重开刷属性」游戏，而更像一场 **可复盘的人生沙盘推演**：

- 每个选择都会改变 **金钱、精力、喜悦** 三维属性
- 事件由 **DeepSeek AI** 实时生成（也可降级到预设事件库），每局体验不同
- 中央 **翻牌抽卡** 带来仪式感——背面是「？」，翻开才是命运
- 70 岁收官时，AI 会根据你的决策轨迹写一段 **200–300 字人生总结**
- 已完成的对局会进入 **历史档案**，随时回看、随时「基于此重开」

适合：想轻量体验「如果当初选另一条路会怎样」的成年人；也适合作为 AI + 产品设计的 Demo 项目。

---

## 设计思路

### 视觉：Playful Geometric（俏皮几何）

采用 **沉静人生沙盘 + 卡牌翻牌** 的融合方案（PRD 中的 B+C）：

| 元素 | 设计 |
|------|------|
| 整体气质 | 暖奶油底、2px 描边、硬阴影，轻松但不幼稚 |
| 生活圈 | 暖粉 / 珊瑚色系 |
| 事业圈 | 靛蓝 / 紫色系 |
| 对局布局 | 左时间轴 · 中翻牌区 · 右主题选择 · 顶栏三维属性 |
| 交互亮点 | 卡片 `rotateY` 翻转 0.6s，揭晓事件与选项 |

高保真原型见 [`docs/prototypes/index.html`](docs/prototypes/index.html)。

### 机制：双圈 × 8 阶段 × AI 事件

```
22岁 ──→ … ──→ 70岁
  │              │
  ├─ 生活圈（8 子主题）   父母 / 子女 / 对象 / 身体健康 …
  └─ 事业圈（8 子主题）   工作 / 创业 / 副业 / 地产 …
```

- **策略可读**：左侧 8 轮时间轴始终可见，属性变化即时反馈
- **随机但不失控**：年龄段决定「能选多细」——越年轻选项越多，越年长越交给命运
- **AI Native**：事件与回顾由 LLM 生成；API 不可用时自动降级，游戏不中断

### 经济：工资与就业

- 默认 **在职**，每轮结束发放 **年薪 × 本轮年数** 的固定工资
- 初始年薪 **10 万**，每进入下一轮年薪 **+12%**
- 选择 **创业** 或 **失业** 类选项后，该阶段 **无固定工资**（仍可通过事件选项增减金钱）
- 选择 **「工作」** 主题并继续上班，可恢复在职状态

---

## 怎么玩？

### 1. 注册 / 登录

使用邮箱注册账号，登录后进入首页。

### 2. 创建角色

- 输入 **角色姓名**（仅存本地浏览器，用于展示）
- 可调 **初始金钱 / 精力 / 喜悦**（默认 50000 / 10 / 0）
- 点击「开始人生」

### 3. 对局主流程（核心）

每一 **人生阶段（轮次）** 的流程：

1. **选圈子**：生活圈 或 事业圈  
2. **选子主题**（按年龄段规则，见下表）  
3. **翻牌抽事件**：点击「翻牌抽事件」，AI 生成一张事件卡  
4. **做抉择**：2–3 个选项，每个选项会 ± 金钱 / 精力 / 喜悦  
5. 完成本轮全部事件后，**自动进入下一年龄段**（并结算工资）

#### 年龄段与抽卡规则

| 轮次 | 年龄 | 每轮事件数 | 选圈/主题规则 |
|:----:|:-----|:----------:|:-------------|
| 1–4 | 22–40 岁 | 2 | 自选圈子 + 自选子主题 |
| 5–7 | 40–60 岁 | 2 | 只选圈子，子主题随机 |
| 8 | 60–70 岁 | 1 | 圈子 + 主题全随机 |

#### 16 个子主题

**生活圈：** 父母 · 子女 · 对象 · 身体健康 · 消费娱乐 · 自我觉察 · 亲情爱情 · 友情  

**事业圈：** 工作 · 创业 · 副业 · 感性 · 地产 · 理性 · 公益 · 保险信托

### 4. 人生回顾

第 8 轮最后一个选择完成后，游戏结束：

- 展示 **结局标签**（如「平衡人生」「事业达人」）
- **AI 人生总结** 全文
- **关键抉择** 时间轴

### 5. 历史档案

首页 → 「历史人生档案」：

- 浏览已完成的对局列表
- 点进详情查看完整轨迹
- 「基于此重开」→ 创建新角色再来一局

---

## 技术栈

| 层 | 技术 |
|----|------|
| 前端 | React 18 · TypeScript · Vite · Ant Design |
| 后端 | Python 3.11+ · FastAPI · PyCore · SQLite |
| AI | DeepSeek API（事件生成 + 人生回顾） |
| 认证 | JWT + bcrypt |

---

## 本地运行

### 在线演示（Mock）

GitHub Pages 托管 **Mock 演示版**（无需后端，数据为本地模拟）：

**https://guisiyu99.github.io/Life-Restart-sandbox/**

> 推送 `main` 分支后由 GitHub Actions 自动构建部署。仓库 Settings → Pages → Source 需选 **GitHub Actions**。

### 环境要求

- Node.js 18+
- Python 3.11+
- （可选）DeepSeek API Key — 无 Key 时走预设事件与模板总结

### 1. 克隆仓库

```bash
git clone git@github.com:guisiyu99/Life-Restart-sandbox.git
cd Life-Restart-sandbox
```

### 2. 后端

```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r backend/requirements.txt

cp backend/.env.example backend/.env
# 编辑 backend/.env，填入 LLM_API_KEY（可选）、JWT_SECRET

cd backend
PYTHONPATH=.:.. python -m uvicorn src.main:app --host 127.0.0.1 --port 8099 --reload
```

### 3. 前端

```bash
cd frontend
npm install
cp .env.example .env

npm run dev
# 打开 http://localhost:5199
```

### 4. 运行测试

```bash
cd backend
PYTHONPATH=.:.. python -m pytest tests/ -q
```

---

## 项目结构

```
├── frontend/          # React 前端（端口 5199）
├── backend/           # FastAPI 后端（端口 8099）
├── pycore/            # 内部 Python 框架
├── docs/              # PRD、API 契约、原型、开发计划
│   └── prototypes/    # 高保真 HTML 原型
└── .sdd/              # SDD 任务、经验、Bugfix 报告
```

更完整的接口说明见 [`docs/api-contracts.md`](docs/api-contracts.md)，产品设计见 [`docs/PRD.md`](docs/PRD.md)。

---

## 环境变量说明

| 文件 | 用途 |
|------|------|
| `backend/.env` | **本地配置，勿提交 Git** — LLM API Key、JWT Secret、数据库等 |
| `backend/.env.example` | 配置模板（空 Key，可安全提交） |
| `frontend/.env` | 前端 Mock 开关、API 代理目标 |
| `frontend/.env.example` | 前端配置模板 |

---

## 许可证与说明

本项目为 **人生决策模拟 MVP**，由 [SDD V7.1](https://github.com/guisiyu99/Life-Restart-sandbox) 流程驱动开发。

- 游戏事件内容为 AI 生成或预设虚构场景，不代表真实建议
- 所有选择都是最好的安排 ✨

---

© 2026 重启人生沙盘模拟
