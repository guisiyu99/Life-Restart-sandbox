# Stitch Prototype Prompts — Life Restart Sandbox Simulator

**Project**: 重启人生沙盘模拟 (Life Restart Sandbox Simulator)  
**Platform**: Desktop Web  
**Viewport**: 1440 × 900  
**Language**: All UI copy, labels, buttons, and sample data must be **Simplified Chinese**. No English placeholder text in the UI.

---

## How to Use

1. Copy the **Global Design Context** block first (paste once at the start of a Stitch session, or prepend to each screen prompt).
2. Generate **one screen at a time** using the numbered prompts below (recommended for best quality).
3. After export, unzip to `docs/prototypes/` following the folder naming in phase-B2.

---

## Global Design Context (paste with every screen)

```
You are an expert UI/UX designer and frontend engineer. Design a desktop web prototype for a life-restart sandbox simulation game called "重启人生沙盘模拟" (Life Restart Sandbox Simulator). Target users are 18+ adults who want to explore alternate life paths through choices across 8 life stages (ages 22–70).

Apply the **Playful Geometric** design system — friendly, tactile, pop, energetic. Core concept: "Stable Grid, Wild Decoration." Content areas are clean and readable; surrounding decoration uses primitive shapes, patterns, and hard shadows.

DESIGN TOKENS (Light Mode):
- background: #FFFDF5 (warm cream paper)
- foreground: #1E293B (slate 800)
- muted: #F1F5F9 | mutedForeground: #64748B
- accent (primary): #8B5CF6 (vivid violet)
- secondary: #F472B6 (hot pink — use for Life Circle / 生活圈)
- tertiary: #FBBF24 (amber — highlights, money)
- quaternary: #34D399 (emerald — energy/stamina)
- border: #E2E8F0 | card: #FFFFFF | ring: #8B5CF6

TYPOGRAPHY:
- Headings: "Outfit", Bold/ExtraBold 700–800
- Body: "Plus Jakarta Sans", Regular 400 / Medium 500
- Type scale ratio: 1.25

SHAPE & EFFECTS:
- Border width: 2px chunky borders
- Radius: sm 8px, md 16px, lg 24px, full pill 9999px
- Hard shadow (no blur): 4px 4px 0 #1E293B; hover 6px 6px; active 2px 2px
- Sticker cards: white bg, 2px dark border, rounded-xl, hard offset shadow
- Background decoration: dot grids, confetti shapes (circles, triangles), dashed SVG connectors — do not obstruct text

BUTTONS:
- Primary "Candy Button": accent bg, white bold text, rounded-full, 2px #1E293B border, hard shadow, hover lift
- Secondary: transparent, 2px border, rounded-full, hover fill tertiary yellow

ANIMATION FEEL (show static states + one hover state where relevant):
- Bouncy ease, sticker wiggle on card hover (-1deg rotate, scale 1.02)
- Card flip area should visually suggest a large playable card (3:4 ratio) with gradient back — Life Circle warm pink gradient, Career Circle violet-blue gradient

ICONS: Lucide-style, stroke 2.5px, often inside colored circles.

ACCESSIBILITY: AAA contrast for body text; never rely on color alone; min tap target 48px; respect reduced motion.

LAYOUT: max-w-6xl container, generous spacing py-16–24, 12-column grid grouped into large blocks.

GAME-SPECIFIC COLOR MAPPING:
- 金钱 Money → tertiary amber #FBBF24
- 精力 Energy → quaternary emerald #34D399
- 喜悦 Joy → secondary pink #F472B6
- 生活圈 Life Circle → secondary pink family
- 事业圈 Career Circle → accent violet family

All visible text in Simplified Chinese. Viewport 1440×900.
```

---

## Screen 1 — Login (P01)

```
[Paste Global Design Context above]

Design a **Login page** for the Life Restart Sandbox Simulator.

PAGE PURPOSE: Email + password authentication. Entry point for returning users.

LAYOUT:
- Centered single-column card (sticker card style) on warm cream background with subtle dot-grid pattern and 2–3 floating confetti shapes (small circles/triangles, low opacity).
- Top of card: small game logo mark (abstract geometric life-path icon, not a real brand).
- Title: "欢迎回来"
- Subtitle: "登录后继续你的人生沙盘"

COMPONENTS:
1. Email input — label "邮箱", placeholder "请输入邮箱"
2. Password input — label "密码", placeholder "请输入密码"
3. Primary button — full width, "登录"
4. Text link below — "还没有账号？立即注册"
5. Optional small decorative squiggle underline under the main title

SAMPLE DATA: Pre-fill nothing; show empty fields.

STATES: Show one inline error example below password field in muted red: "邮箱或密码错误，请重试"

Do NOT include: third-party OAuth, social login, forgot-password flow, captcha.

Style: Playful Geometric candy button for login, chunky input borders, hard shadow on card.
```

---

## Screen 2 — Register (P02)

```
[Paste Global Design Context above]

Design a **Registration page** for the Life Restart Sandbox Simulator.

PAGE PURPOSE: Create account with email + password.

LAYOUT: Same visual shell as login — centered sticker card, dot-grid background, confetti decoration.

COMPONENTS:
1. Title: "创建账号"
2. Subtitle: "开启你的第一段虚拟人生"
3. Email input — "邮箱"
4. Password input — "密码"
5. Confirm password input — "确认密码"
6. Primary button — "注册并登录"
7. Link — "已有账号？去登录"

VALIDATION HINT (static example): Small text under confirm field: "两次密码输入不一致"

Do NOT include: phone SMS, email verification code step.

Match login page styling exactly for consistency.
```

---

## Screen 3 — Home (P03)

```
[Paste Global Design Context above]

Design the **Home / Landing page** for logged-in users.

PAGE PURPOSE: Minimal hub — big title, tagline, two primary actions. No dashboard widgets.

LAYOUT:
- Full viewport hero, vertically centered content
- Top-right corner: user menu chip showing "zhang@example.com" + "退出" link
- Background: warm cream with large decorative yellow circle behind title (partial bleed), dot pattern, confetti shapes
- NO sidebar. NO stats cards. NO feature grid.

CONTENT (exact copy):
- **Main title (H1, Outfit ExtraBold, very large)**: 重启人生沙盘模拟
- **Subtitle (Plus Jakarta Sans, muted)**: 八段人生旅程，探索另一种可能
- **Primary button (large candy button, accent violet)**: 创建角色
- **Secondary button (large, outlined, below primary)**: 历史人生档案

Both buttons: min height 56px, rounded-full, hard shadow, side-by-side on desktop OR stacked centered with 16px gap.

DECORATION: Small squiggle SVG under subtitle. Optional tiny geometric icons near buttons (person-plus icon for 创建角色, archive icon for 历史人生档案) inside colored circles.

Do NOT include: navigation bar with multiple tabs, recent game preview, announcements.
```

---

## Screen 4 — Character Creation (P04)

```
[Paste Global Design Context above]

Design the **Character Creation page**.

PAGE PURPOSE: Set name and adjust three starting attributes before starting a new life at age 22.

LAYOUT:
- Top: step indicator "步骤 1 / 1 · 创建角色"
- Left column (60%): form area inside sticker card
- Right column (40%): decorative illustration — abstract geometric character silhouette with floating shape badges

COMPONENTS:
1. Name input
   - Label: "角色姓名"
   - Placeholder: "请输入 2–8 个字符"
   - Sample filled value: "林小然"

2. Attribute panel — title "初始属性" with helper text "可在默认值基础上调整"
   Three stat rows, each with label, numeric display, stepper (+ / −) or slider:

   | Stat | Chinese label | Default value | Suggested range hint |
   |------|---------------|---------------|----------------------|
   | Money | 金钱 | 50,000 | show as "¥50,000" |
   | Energy | 精力值 | 10 | show "10 点" |
   | Joy | 喜悦值 | 0 | show "0" |

   Color-code stat icons: money=amber circle, energy=emerald circle, joy=pink circle.

3. Info callout (small sticker note): "人生从 22 岁开始，共 8 个人生阶段"

4. Bottom actions:
   - Secondary "返回首页"
   - Primary "开始人生"

SAMPLE STATE: Show name "林小然", money 50000, energy 10, joy 0.

Do NOT include: talent card gacha, random roll sets, gender selection, avatar picker.
```

---

## Screen 5 — Game Session / Main Play (P05) ★ Core Screen

```
[Paste Global Design Context above]

Design the **main gameplay screen** — the core sandbox simulation interface. This combines a life-stage timeline (left), a large flip-card event area (center), and circle/theme picker (right).

PAGE PURPOSE: User plays through 8 life rounds. Each round they pick Life or Career circle (and sub-theme when allowed), flip a card to reveal an AI-generated event, then choose 2–3 options that change stats.

TOP BAR (full width, sticky):
- Left: character name "林小然" + age badge "28 岁"
- Center-right: three stat chips with icons:
  - 金钱 ¥128,500 (amber)
  - 精力 7 (emerald, show as fraction or bar hint)
  - 喜悦 3 (pink)
- Far right: round label "第 2 轮 · 25–30 岁"

THREE-COLUMN LAYOUT (below top bar):

**LEFT — Life Timeline (width ~220px)**
Vertical stepper / timeline with 8 stages:
1. 22–25 ✓ (completed, green check in circle)
2. 25–30 ● (current, accent violet, pulsing ring)
3. 30–35 (upcoming, muted)
4. 35–40
5. 40–45
6. 45–50
7. 50–60
8. 60–70

Connect steps with dashed line. Completed steps use quaternary green; current uses accent.

**CENTER — Flip Card Event Area (flex-grow)**
Show the card in **revealed/front state** (design both back hint and front as layered mock):

Card front (visible):
- Small tag pills: "生活圈" (pink) + "友情" (muted pill)
- Event title (bold): "老友婚礼上的抉择"
- Event body (2–3 lines): "大学室友邀请你担任伴郎，但需要请假三天并承担往返费用。你最近项目正忙，精力也所剩不多。"
- Three option buttons (stacked, full width within card):
  - A. "答应前往，维护友情" — hint tags: 精力 −2 · 喜悦 +3
  - B. "礼金祝贺，人不到场" — 金钱 −500 · 喜悦 +1
  - C. "干脆失联，专注工作" — 精力 +1 · 喜悦 −2

Card styling: large 3:4 portrait card, white face, 2px border, pink hard shadow (life event). Show ghost of card back behind with pink-to-coral gradient and geometric pattern.

Above card: progress text "本轮事件 1 / 2"

**RIGHT — Circle & Theme Picker (width ~320px)**
Title: "选择事件主题"

Segment control tabs:
- "生活圈" (active, pink underline)
- "事业圈" (inactive)

Below: 4×2 grid of 8 sub-theme chips for Life Circle (user is under 40, so all themes selectable):
父母 | 子女 | 对象 | 身体健康
消费娱乐 | 自我觉察 | 亲情爱情 | 友情

One chip "友情" is selected (pink fill, white text). Others are outline sticker chips.

Bottom of panel: small rules hint card:
"40 岁前：可选生活/事业及任意子主题，每轮 2 个事件"

DECORATION: Subtle confetti in margins. Do not clutter the card text area.

Do NOT include: chat interface, map, 3D avatar, inventory grid.

This screen must feel like a playful board-game UI with readable event text.
```

---

## Screen 6 — Life Review / Ending (P06)

```
[Paste Global Design Context above]

Design the **Life Review / Ending page** shown when the player completes all 8 rounds (age 70).

PAGE PURPOSE: Show outcome tags, final stats, choice timeline summary, AI-generated narrative paragraph, and actions to replay or go home.

LAYOUT: Single scrolling page, max-w-4xl centered.

SECTIONS:

1. **Hero banner** (arch/blob top shape):
   - Title: "人生回顾"
   - Character: "林小然 · 22—70 岁"
   - Outcome tag pills (rotated slightly, sticker style): "平衡人生" (accent) + "温暖关系" (secondary)

2. **Final stats row** — three sticker cards in a row:
   - 金钱 ¥2,340,000
   - 精力 4
   - 喜悦 8
   Each with mini horizontal bar visualization.

3. **AI Summary card** (featured, pink shadow):
   - Header with sparkle icon: "AI 人生总结"
   - Body paragraph (Chinese, 3–4 lines): "林小然的一生在事业与亲情之间寻找平衡。30 岁后的几次关键选择让你既保持了稳定收入，也未曾疏远老友与家人。晚年的你回首过往，虽非耀眼传奇，却拥有了真实可触的幸福瞬间。"

4. **Choice timeline** — vertical list, compact:
   Title: "关键抉择"
   Show 4 sample rows ( imply 15 total):
   - 22–25 · 工作 · "接受外派机会" → 金钱 +8000
   - 25–30 · 友情 · "婚礼到场" → 喜悦 +3
   - 40–45 · 父母 · "接父母同住" → 精力 −2 · 喜悦 +4
   - 50–60 · 公益 · "参与社区项目" → 喜悦 +2

5. **Action buttons** (centered):
   - Primary: "再来一次"
   - Secondary: "返回首页"

Background: celebratory but readable — scattered small geometric shapes, no overwhelming confetti on text.

Do NOT include: share to social, leaderboard, compare with friends.
```

---

## Screen 7 — History Archive List (P07)

```
[Paste Global Design Context above]

Design the **History Archive List page** ("历史人生档案").

PAGE PURPOSE: List all completed life runs for the logged-in user, newest first.

LAYOUT:
- Top bar: back link "← 返回首页" + page title "历史人生档案"
- Main: vertical list of sticker cards (NOT a dense table)

SAMPLE DATA — at least 3 cards:

Card 1:
- Name: "林小然"
- Date: "2026-06-07 14:32"
- Outcome tag: "平衡人生"
- One-line summary: "金钱 ¥234万 · 喜悦 8 · 共 15 次抉择"
- Chevron right affordance

Card 2:
- Name: "陈野"
- Date: "2026-06-05 09:18"
- Outcome tag: "事业达人"
- Summary: "金钱 ¥580万 · 喜悦 4 · 共 15 次抉择"

Card 3:
- Name: "苏晚"
- Date: "2026-06-01 21:05"
- Outcome tag: "温暖关系"
- Summary: "金钱 ¥86万 · 喜悦 10 · 共 15 次抉择"

Cards alternate subtle header accent colors (violet, pink, yellow) on the left border stripe.

EMPTY STATE (show as small inset mock or second artboard note): Illustration + "暂无人生档案" + button "创建角色"

Do NOT include: delete, search, filter, pagination controls (V1 shows all).
```

---

## Screen 8 — History Detail (P08)

```
[Paste Global Design Context above]

Design the **History Detail / Replay page** for a single completed life run.

PAGE PURPOSE: Read-only view of a past game — same information as P06 Life Review but accessed from archive.

LAYOUT:
- Top: back "← 返回档案列表" + meta "游玩于 2026-06-07 14:32"
- Reuse P06 sections: hero with name/tags, final stats, AI summary, full choice timeline

DIFFERENCE from P06:
- Replace action buttons with:
  - Primary: "基于此重开" (helper: 姓名将预填为 "林小然")
  - Secondary: "返回档案列表"
- Add small readonly badge: "历史记录" (muted pill)

Show **6 timeline rows** (more than P06 preview) to imply full record.

Sample AI summary (different text from P06 to show variation):
"陈野的一生几乎与事业绑定。从 25 岁起的选择不断放大财富积累，却也几次错过亲密关系的深化。70 岁的你站在终点，钱包丰厚，内心却偶有空虚——这是选择的结果，而非失败。"

Character name on this screen: "陈野", tags: "事业达人" + "孤独终老"
Stats: 金钱 ¥5,800,000 · 精力 3 · 喜悦 4
```

---

## Optional: Game Session — Age 40+ Variant (P05-B)

```
[Paste Global Design Context above]

Design an **alternate state of the main gameplay screen (P05)** for mid-life round (age 40–60 rules).

Same layout as P05, but RIGHT PANEL changes:
- Title: "选择事件圈子"
- ONLY two large sticker buttons: "生活圈" (selected) | "事业圈"
- NO sub-theme grid — instead show muted info box: "40–60 岁：仅可选择生活或事业，子主题由系统随机"
- Center card tag shows random assignment: "生活圈 · 父母" (system picked)

Round label: "第 5 轮 · 40–45 岁"
Progress: "本轮事件 2 / 2"

Use this artboard to document the restricted picker UI state.
```

---

## Optional: Game Session — Age 60+ Variant (P05-C)

```
[Paste Global Design Context above]

Design an **alternate state of the main gameplay screen (P05)** for senior round (age 60–70 rules).

Same layout as P05, but:
- RIGHT PANEL hidden OR replaced with locked decorative panel: dashed border, lock icon, text "60 岁后：事件完全随机，无需选择"
- Center card tags: "随机事件 · 身体健康"
- Progress: "本轮事件 1 / 1"
- Round label: "第 8 轮 · 60–70 岁"

Card event example:
Title: "年度体检报告"
Body: "医生提示你需要调整作息。家人希望你能搬去与他们同住。"
Options: A / B / C with stat hints.

Shows the simplest end-stage UX.
```

---

## Full Flow Prompt (single-shot alternative)

If Stitch supports multi-screen generation in one prompt, use this condensed version:

```
[Paste Global Design Context above]

Generate a **8-screen desktop web prototype (1440×900)** for "重启人生沙盘模拟", a Chinese life-restart sandbox game. Apply Playful Geometric design system throughout (warm cream #FFFDF5 bg, violet accent #8B5CF6, pink #F472B6 for life, hard 4px shadows, Outfit + Plus Jakarta Sans, sticker cards, dot-grid decoration).

Screens:
1. Login — email/password, 登录
2. Register — email/password/confirm, 注册并登录
3. Home — ONLY large title "重启人生沙盘模拟", subtitle "八段人生旅程，探索另一种可能", two big buttons "创建角色" and "历史人生档案"
4. Character Creation — name + three stats (金钱 default 50000, 精力 10, 喜悦 0) with adjusters, 开始人生
5. Game Main — top stat bar, left 8-step timeline, center large flip-card with event + 3 choices, right life/career theme picker (16 sub-themes in 4×2 grid)
6. Life Review — outcome tags, final stats, AI summary paragraph, choice timeline, 再来一次 / 返回首页
7. History List — 3 archive cards with name/date/outcome
8. History Detail — same as review but read-only, 基于此重开

All UI text in Simplified Chinese. Include realistic sample data. No English placeholders.
```

---

## Reference Notes for Stitch

| Item | Value |
|------|-------|
| Life circles | 生活圈 (8 themes) / 事业圈 (8 themes) |
| Life themes | 父母, 子女, 对象, 身体健康, 消费娱乐, 自我觉察, 亲情爱情, 友情 |
| Career themes | 工作, 创业, 副业, 感性, 地产, 理性, 公益, 保险信托 |
| Age rounds | 22–25, 25–30, 30–35, 35–40, 40–45, 45–50, 50–60, 60–70 |
| Events per round | 2 (before 60), 1 (60–70) |
| AI | DeepSeek generates events & summary (not visible in UI except "AI 人生总结" label) |
| Visual fusion | B sandbox layout + C large flip-card center |
| Competitor mood | Cleaner than 人生重开模拟器 dark minimal; more playful than NeoLife dashboard |

---

*Generated for SDD project `life-restart-sandbox`. After Stitch export, place files under `docs/prototypes/`.*
