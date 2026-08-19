"""DeepSeek AI 事件生成服务。"""

from __future__ import annotations

import json
import re
from typing import Any

import httpx

from pycore.core import get_logger
from src.core.config import settings

logger = get_logger()


def _chat_completions_url() -> str:
    base = settings.llm_base_url.rstrip("/")
    if base.endswith("/v1"):
        return f"{base}/chat/completions"
    return f"{base}/v1/chat/completions"


def _extract_json(content: str) -> dict[str, Any]:
    text = content.strip()
    fence = re.search(r"```(?:json)?\s*([\s\S]*?)```", text)
    if fence:
        text = fence.group(1).strip()
    data = json.loads(text)
    if not isinstance(data, dict):
        raise ValueError("AI response is not a JSON object")
    return data


def _build_prompt(
    *,
    age_range: str,
    age_round: int,
    circle: str,
    theme: str,
    money: int,
    energy: int,
    joy: int,
) -> str:
    circle_label = "生活圈" if circle == "life" else "事业圈"
    return f"""你是人生模拟游戏的事件编剧。请根据以下上下文生成 ONE 个人生事件 JSON。

## 上下文
- 年龄段：{age_range} 岁（第 {age_round} 轮）
- 圈子：{circle_label}
- 子主题：{theme}
- 当前属性：金钱 {money}，精力 {energy}，喜悦 {joy}

## 输出要求
只输出 JSON，不要 markdown，不要解释。格式：
{{
  "title": "事件标题（10-20字）",
  "description": "事件描述（80-150字，第二人称）",
  "options": [
    {{
      "text": "选项文案",
      "money_change": 整数（-50000 到 50000）,
      "energy_change": 整数（-5 到 5）,
      "joy_change": 整数（-5 到 5）
    }}
  ]
}}

规则：
- options 数量 2 或 3 个
- 文案全中文，贴近中国都市生活
- 属性变化要合理，与选项语义一致
"""


class AIService:
    """调用 DeepSeek 生成事件。"""

    async def generate_event(
        self,
        *,
        age_range: str,
        age_round: int,
        circle: str,
        theme: str,
        money: int,
        energy: int,
        joy: int,
    ) -> dict[str, Any]:
        if not settings.llm_api_key:
            raise RuntimeError("LLM_API_KEY not configured")

        prompt = _build_prompt(
            age_range=age_range,
            age_round=age_round,
            circle=circle,
            theme=theme,
            money=money,
            energy=energy,
            joy=joy,
        )

        payload = {
            "model": settings.llm_model,
            "messages": [
                {"role": "system", "content": "你是严谨的游戏事件生成器，只输出合法 JSON。"},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.8,
            "response_format": {"type": "json_object"},
        }

        async with httpx.AsyncClient(trust_env=False, timeout=60.0) as client:
            response = await client.post(
                _chat_completions_url(),
                headers={
                    "Authorization": f"Bearer {settings.llm_api_key}",
                    "Content-Type": "application/json",
                },
                json=payload,
            )
            response.raise_for_status()
            body = response.json()

        content = body["choices"][0]["message"]["content"]
        parsed = _extract_json(content)
        logger.info("AI event generated", theme=theme, age_round=age_round)
        return parsed

    async def generate_life_review(
        self,
        *,
        decisions: list[dict[str, Any]],
        money: int,
        energy: int,
        joy: int,
    ) -> str:
        if not settings.llm_api_key:
            raise RuntimeError("LLM_API_KEY not configured")

        decision_lines = []
        for item in decisions[:15]:
            age_range = item.get("age_range", "")
            theme = item.get("theme", "")
            title = item.get("event_title", "")
            chosen = item.get("chosen_option", "")
            decision_lines.append(f"- {age_range}岁·{theme}：{title} → {chosen}")
        summary = "\n".join(decision_lines) if decision_lines else "- 暂无详细决策记录"

        prompt = f"""你是人生模拟游戏的回顾作家。根据玩家 22-70 岁的关键抉择，写一段 200-300 字的中文人生总结。

## 最终属性
- 金钱：{money}
- 精力：{energy}
- 喜悦：{joy}

## 关键抉择（节选）
{summary}

## 要求
- 第二人称「你」
- 200-300 字，有情感温度
- 可提及财富/健康/关系等维度，可用 ★ 评级
- 只输出总结正文，不要标题、不要 JSON、不要 markdown"""

        payload = {
            "model": settings.llm_model,
            "messages": [
                {"role": "system", "content": "你是人生回顾撰写者，只输出中文总结正文。"},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.7,
        }

        async with httpx.AsyncClient(trust_env=False, timeout=60.0) as client:
            response = await client.post(
                _chat_completions_url(),
                headers={
                    "Authorization": f"Bearer {settings.llm_api_key}",
                    "Content-Type": "application/json",
                },
                json=payload,
            )
            response.raise_for_status()
            body = response.json()

        content = str(body["choices"][0]["message"]["content"]).strip()
        if not content:
            raise ValueError("Empty AI review")
        logger.info("AI life review generated", decision_count=len(decisions))
        return content
