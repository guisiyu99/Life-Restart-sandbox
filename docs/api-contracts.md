# 接口契约文档

> 版本：V1.0  
> 日期：2026-06-07  
> 状态：前端 Mock 和后端实现的唯一对齐依据。任何变更必须同步更新本文件。

---

## 一、通用约定

### 1.1 统一响应格式

**成功响应：**
```json
{
  "code": 200,
  "message": "success",
  "data": { /* 业务数据 */ }
}
```

**错误响应：**
```json
{
  "code": 4001,
  "message": "具体错误描述",
  "data": null
}
```

**分页响应：**
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "items": [ /* 列表项 */ ],
    "total": 100,
    "page": 1,
    "page_size": 20
  }
}
```

### 1.2 通用错误码

| 错误码 | 说明 |
|--------|------|
| 200 | 成功 |
| 4000 | 请求参数错误 |
| 4001 | 认证失败（用户名或密码错误） |
| 4002 | Token 无效或过期 |
| 4003 | 用户已存在 |
| 4004 | 资源不存在 |
| 4005 | 游戏状态错误（如已完成的游戏不能继续） |
| 5000 | 服务器内部错误 |
| 5001 | 数据库错误 |
| 5002 | 外部服务调用失败（DeepSeek API） |

### 1.3 认证方式

所有需要认证的接口（除注册/登录外）必须在 HTTP Header 中携带：

```
Authorization: Bearer <JWT_TOKEN>
```

---

## 二、接口清单

### 2.1 认证模块

#### POST /api/auth/register

**描述：**用户注册

**请求体：**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**请求体字段说明：**
- `email`：字符串，必填，邮箱格式
- `password`：字符串，必填，最小长度 6 字符

**响应（成功 200）：**
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer",
    "user": {
      "id": 1,
      "email": "user@example.com",
      "created_at": "2026-06-07T15:30:00Z"
    }
  }
}
```

**响应（失败 4003）：**
```json
{
  "code": 4003,
  "message": "用户已存在",
  "data": null
}
```

---

#### POST /api/auth/login

**描述：**用户登录

**请求体：**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**请求体字段说明：**
- `email`：字符串，必填
- `password`：字符串，必填

**响应（成功 200）：**
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer",
    "user": {
      "id": 1,
      "email": "user@example.com",
      "created_at": "2026-06-07T15:30:00Z"
    }
  }
}
```

**响应（失败 4001）：**
```json
{
  "code": 4001,
  "message": "用户名或密码错误",
  "data": null
}
```

---

#### GET /api/auth/me

**描述：**获取当前登录用户信息

**请求头：**
```
Authorization: Bearer <TOKEN>
```

**响应（成功 200）：**
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "id": 1,
    "email": "user@example.com",
    "created_at": "2026-06-07T15:30:00Z"
  }
}
```

**响应（失败 4002）：**
```json
{
  "code": 4002,
  "message": "Token 无效或过期",
  "data": null
}
```

---

### 2.2 游戏模块

#### POST /api/games

**描述：**创建新游戏

**请求头：**
```
Authorization: Bearer <TOKEN>
```

**请求体：**无

**响应（成功 200）：**
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "id": 1,
    "user_id": 1,
    "status": "in_progress",
    "age_round": 1,
    "age_range": "22-25",
    "money": 50000,
    "energy": 10,
    "joy": 0,
    "decisions": [],
    "ai_review": null,
    "created_at": "2026-06-07T15:30:00Z",
    "updated_at": "2026-06-07T15:30:00Z"
  }
}
```

**响应字段说明：**
- `id`：游戏 ID
- `status`：游戏状态（`in_progress` / `completed`）
- `age_round`：当前年龄段（1-8）
- `age_range`：年龄区间字符串（如 "22-25"）
- `money`：金钱属性
- `energy`：精力属性
- `joy`：快乐度属性
- `decisions`：历史决策数组
- `ai_review`：AI 生成的人生总结（仅 completed 状态有值）

---

#### GET /api/games/{game_id}

**描述：**获取游戏详情

**请求头：**
```
Authorization: Bearer <TOKEN>
```

**路径参数：**
- `game_id`：整数，游戏 ID

**响应（成功 200）：**
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "id": 1,
    "user_id": 1,
    "status": "in_progress",
    "age_round": 3,
    "age_range": "31-35",
    "money": 120000,
    "energy": 8,
    "joy": 15,
    "decisions": [
      {
        "round": 1,
        "age_range": "22-25",
        "circle": "career",
        "theme": "工作机会",
        "event_title": "接受大厂 Offer",
        "event_description": "你收到了一家互联网大厂的 Offer，月薪 15000，但需要每天加班到晚上 10 点。",
        "chosen_option": "接受 Offer",
        "money_change": 30000,
        "energy_change": -2,
        "joy_change": 5
      }
    ],
    "ai_review": null,
    "created_at": "2026-06-07T15:30:00Z",
    "updated_at": "2026-06-07T16:00:00Z"
  }
}
```

**响应（失败 4004）：**
```json
{
  "code": 4004,
  "message": "游戏不存在",
  "data": null
}
```

---

#### POST /api/games/{game_id}/draw-event

**描述：**抽取事件

**请求头：**
```
Authorization: Bearer <TOKEN>
```

**路径参数：**
- `game_id`：整数，游戏 ID

**请求体：**
```json
{
  "circle": "life",
  "theme": "健康管理"
}
```

**请求体字段说明：**
- `circle`：字符串，可选，生活圈（"life"）或职业圈（"career"）
  - 40 岁前（age_round 1-4）：必填
  - 40-60 岁（age_round 5-6）：必填
  - 60 岁后（age_round 7-8）：不填（系统随机）
- `theme`：字符串，可选，子主题名称
  - 40 岁前（age_round 1-4）：必填
  - 40 岁后：不填

**响应（成功 200）：**
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "events": [
      {
        "event_id": "evt_001",
        "title": "体检发现血压偏高",
        "description": "年度体检报告显示你的血压达到 140/90，医生建议调整生活方式。",
        "options": [
          {
            "option_id": "opt_001",
            "text": "立即开始健身计划，每周运动 3 次",
            "money_change": -5000,
            "energy_change": 3,
            "joy_change": 2
          },
          {
            "option_id": "opt_002",
            "text": "购买保健品，但不改变生活习惯",
            "money_change": -3000,
            "energy_change": 0,
            "joy_change": -1
          },
          {
            "option_id": "opt_003",
            "text": "忽略医生建议，继续原来的生活",
            "money_change": 0,
            "energy_change": -1,
            "joy_change": 0
          }
        ]
      },
      {
        "event_id": "evt_002",
        "title": "朋友邀请参加马拉松训练",
        "description": "你的朋友正在准备半程马拉松，邀请你一起训练。",
        "options": [
          {
            "option_id": "opt_004",
            "text": "欣然接受，报名参赛",
            "money_change": -2000,
            "energy_change": 4,
            "joy_change": 6
          },
          {
            "option_id": "opt_005",
            "text": "婉拒邀请，保持现状",
            "money_change": 0,
            "energy_change": 0,
            "joy_change": 0
          }
        ]
      }
    ],
    "count": 2
  }
}
```

**响应字段说明：**
- `events`：事件数组（根据年龄段规则返回 1-2 个事件）
  - `event_id`：事件唯一标识（前端用于区分卡片）
  - `title`：事件标题
  - `description`：事件描述
  - `options`：选项数组（2-3 个选项）
    - `option_id`：选项唯一标识
    - `text`：选项文案
    - `money_change`：金钱变化
    - `energy_change`：精力变化
    - `joy_change`：快乐度变化
- `count`：事件数量

**响应（失败 4005）：**
```json
{
  "code": 4005,
  "message": "游戏已完成，无法继续",
  "data": null
}
```

---

#### POST /api/games/{game_id}/choices

**描述：**提交选择

**请求头：**
```
Authorization: Bearer <TOKEN>
```

**路径参数：**
- `game_id`：整数，游戏 ID

**请求体：**
```json
{
  "event_id": "evt_001",
  "option_id": "opt_001",
  "circle": "life",
  "theme": "健康管理",
  "event_title": "体检发现血压偏高",
  "event_description": "年度体检报告显示你的血压达到 140/90，医生建议调整生活方式。",
  "chosen_option_text": "立即开始健身计划，每周运动 3 次",
  "money_change": -5000,
  "energy_change": 3,
  "joy_change": 2
}
```

**请求体字段说明：**
- `event_id`：字符串，事件 ID
- `option_id`：字符串，选项 ID
- `circle`：字符串，圈类型（"life" / "career"）
- `theme`：字符串，子主题名称
- `event_title`：字符串，事件标题
- `event_description`：字符串，事件描述
- `chosen_option_text`：字符串，选中的选项文案
- `money_change`：整数，金钱变化
- `energy_change`：整数，精力变化
- `joy_change`：整数，快乐度变化

**响应（成功 200）：**
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "id": 1,
    "age_round": 1,
    "age_range": "22-25",
    "money": 45000,
    "energy": 13,
    "joy": 2,
    "last_decision": {
      "round": 1,
      "age_range": "22-25",
      "circle": "life",
      "theme": "健康管理",
      "event_title": "体检发现血压偏高",
      "event_description": "年度体检报告显示你的血压达到 140/90，医生建议调整生活方式。",
      "chosen_option": "立即开始健身计划，每周运动 3 次",
      "money_change": -5000,
      "energy_change": 3,
      "joy_change": 2
    }
  }
}
```

**响应字段说明：**
- `id`：游戏 ID
- `age_round`：当前年龄段
- `age_range`：年龄区间
- `money`：更新后的金钱
- `energy`：更新后的精力
- `joy`：更新后的快乐度
- `last_decision`：本次决策记录

---

#### POST /api/games/{game_id}/advance-round

**描述：**进入下一年龄段

**请求头：**
```
Authorization: Bearer <TOKEN>
```

**路径参数：**
- `game_id`：整数，游戏 ID

**请求体：**无

**响应（成功 200）：**
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "id": 1,
    "age_round": 2,
    "age_range": "26-30",
    "money": 45000,
    "energy": 13,
    "joy": 2,
    "status": "in_progress"
  }
}
```

**响应字段说明：**
- `id`：游戏 ID
- `age_round`：新的年龄段（+1）
- `age_range`：新的年龄区间
- `money`：当前金钱
- `energy`：当前精力
- `joy`：当前快乐度
- `status`：游戏状态

---

#### POST /api/games/{game_id}/finish

**描述：**完成游戏并生成 AI 回顾

**请求头：**
```
Authorization: Bearer <TOKEN>
```

**路径参数：**
- `game_id`：整数，游戏 ID

**请求体：**无

**响应（成功 200）：**
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "id": 1,
    "status": "completed",
    "age_round": 8,
    "age_range": "66-70",
    "money": 230000,
    "energy": 5,
    "joy": 68,
    "ai_review": "你的一生充满了勇敢的选择。从 22 岁接受大厂 Offer 开始，你在职场上稳步前进，虽然透支了一些精力，但换来了可观的财富积累。中年时期你开始注重健康管理，精力逐渐恢复。退休后你将更多时间投入到兴趣爱好和家庭陪伴，快乐度持续攀升。总体来看，这是一段平衡且充实的人生旅程，财富自由度★★★★☆，幸福感★★★★★，遗憾度★★☆☆☆。",
    "created_at": "2026-06-07T15:30:00Z",
    "updated_at": "2026-06-07T18:00:00Z"
  }
}
```

**响应字段说明：**
- `ai_review`：AI 生成的 200-300 字人生总结
- 其他字段同游戏详情

**响应（失败 5002）：**
```json
{
  "code": 5002,
  "message": "AI 服务调用失败，返回默认总结",
  "data": {
    "id": 1,
    "status": "completed",
    "ai_review": "你走过了完整的人生旅程。最终财富：230000，精力：5，快乐度：68。这是属于你的独特人生。",
    "money": 230000,
    "energy": 5,
    "joy": 68
  }
}
```

---

### 2.3 归档模块

#### GET /api/archives

**描述：**获取历史游戏列表（已完成的游戏）

**请求头：**
```
Authorization: Bearer <TOKEN>
```

**查询参数：**
- `page`：整数，可选，页码（默认 1）
- `page_size`：整数，可选，每页数量（默认 20）

**响应（成功 200）：**
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "items": [
      {
        "id": 1,
        "status": "completed",
        "money": 230000,
        "energy": 5,
        "joy": 68,
        "ai_review": "你的一生充满了勇敢的选择...",
        "created_at": "2026-06-07T15:30:00Z",
        "updated_at": "2026-06-07T18:00:00Z"
      },
      {
        "id": 2,
        "status": "completed",
        "money": 80000,
        "energy": 12,
        "joy": 45,
        "ai_review": "你选择了稳定的人生路径...",
        "created_at": "2026-06-06T10:00:00Z",
        "updated_at": "2026-06-06T12:30:00Z"
      }
    ],
    "total": 2,
    "page": 1,
    "page_size": 20
  }
}
```

**响应字段说明：**
- `items`：归档游戏数组
  - `id`：游戏 ID
  - `money`：最终金钱
  - `energy`：最终精力
  - `joy`：最终快乐度
  - `ai_review`：AI 总结（摘要，完整内容需调用详情接口）
  - `created_at`：创建时间
  - `updated_at`：完成时间
- `total`：总记录数
- `page`：当前页码
- `page_size`：每页数量

---

#### GET /api/archives/{game_id}

**描述：**获取归档游戏详情（包含完整决策轨迹）

**请求头：**
```
Authorization: Bearer <TOKEN>
```

**路径参数：**
- `game_id`：整数，游戏 ID

**响应（成功 200）：**
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "id": 1,
    "status": "completed",
    "money": 230000,
    "energy": 5,
    "joy": 68,
    "ai_review": "你的一生充满了勇敢的选择。从 22 岁接受大厂 Offer 开始，你在职场上稳步前进...",
    "decisions": [
      {
        "round": 1,
        "age_range": "22-25",
        "circle": "career",
        "theme": "工作机会",
        "event_title": "接受大厂 Offer",
        "event_description": "你收到了一家互联网大厂的 Offer，月薪 15000，但需要每天加班到晚上 10 点。",
        "chosen_option": "接受 Offer",
        "money_change": 30000,
        "energy_change": -2,
        "joy_change": 5
      },
      {
        "round": 1,
        "age_range": "22-25",
        "circle": "life",
        "theme": "健康管理",
        "event_title": "体检发现血压偏高",
        "event_description": "年度体检报告显示你的血压达到 140/90，医生建议调整生活方式。",
        "chosen_option": "立即开始健身计划，每周运动 3 次",
        "money_change": -5000,
        "energy_change": 3,
        "joy_change": 2
      }
    ],
    "created_at": "2026-06-07T15:30:00Z",
    "updated_at": "2026-06-07T18:00:00Z"
  }
}
```

**响应字段说明：**
- 完整的游戏数据，包含所有决策记录
- `decisions`：完整决策数组（按 round 排序）

**响应（失败 4004）：**
```json
{
  "code": 4004,
  "message": "归档记录不存在",
  "data": null
}
```

---

### 2.4 健康检查

#### GET /health

**描述：**服务健康检查

**请求头：**无需认证

**响应（成功 200）：**
```json
{
  "status": "healthy",
  "timestamp": "2026-06-07T15:30:00Z",
  "version": "1.0.0"
}
```

**注意：**此接口不使用统一响应格式，直接返回健康状态对象。

---

## 三、前端 Mock 规则

### 3.1 Mock 数据约束

1. **字段子集原则：**Mock 数据字段必须是本文档已定义字段的子集，禁止添加未定义字段
2. **类型一致性：**字段类型必须与本文档完全一致（字符串、整数、数组等）
3. **响应格式统一：**所有 Mock handler 必须返回统一响应格式（code/message/data）
4. **显式 DTO 构造：**Mock handler 不得直接返回内部实体对象，必须按 endpoint 显式构造响应 DTO

### 3.2 Mock 数据示例

**错误示例（禁止）：**
```typescript
// ❌ 添加了未定义字段 display_name
mockGames.push({
  id: 1,
  display_name: "我的游戏", // 未定义字段
  money: 50000
});

// ❌ 直接返回内部实体
return { code: 200, data: gameEntity };
```

**正确示例：**
```typescript
// ✅ 只使用已定义字段
const gameDTO = {
  id: game.id,
  user_id: game.user_id,
  status: game.status,
  age_round: game.age_round,
  age_range: game.age_range,
  money: game.money,
  energy: game.energy,
  joy: game.joy,
  decisions: game.decisions,
  ai_review: game.ai_review,
  created_at: game.created_at,
  updated_at: game.updated_at
};

return { code: 200, message: "success", data: gameDTO };
```

---

## 四、接口变更记录

| 版本 | 日期 | 变更内容 | 影响范围 |
|------|------|---------|---------|
| V1.0 | 2026-06-07 | 初始版本，定义全部 MVP 接口 | 全部接口 |

---

**契约状态：已确认，前后端开发以此为准**
