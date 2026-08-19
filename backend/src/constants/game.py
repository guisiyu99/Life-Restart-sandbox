"""游戏年龄段与主题常量。"""

from __future__ import annotations

import random

AGE_RANGES: dict[int, str] = {
    1: "22-25",
    2: "25-30",
    3: "30-35",
    4: "35-40",
    5: "40-45",
    6: "45-50",
    7: "50-60",
    8: "60-70",
}

EVENTS_PER_ROUND: dict[int, int] = {
    1: 2,
    2: 2,
    3: 2,
    4: 2,
    5: 2,
    6: 2,
    7: 2,
    8: 1,
}

LIFE_THEMES: list[str] = [
    "父母",
    "子女",
    "对象",
    "身体健康",
    "消费娱乐",
    "自我觉察",
    "亲情爱情",
    "友情",
]

CAREER_THEMES: list[str] = [
    "工作",
    "创业",
    "副业",
    "感性",
    "地产",
    "理性",
    "公益",
    "保险信托",
]

ALL_THEMES: list[str] = LIFE_THEMES + CAREER_THEMES

DEFAULT_MONEY = 50000
DEFAULT_ENERGY = 10
DEFAULT_JOY = 0

# 默认在职：初始年薪 10 万，每进入下一轮年薪 +12%
DEFAULT_ANNUAL_SALARY = 100_000
SALARY_GROWTH_PER_ROUND = 0.12

# 各年龄段跨度（年）
YEARS_PER_ROUND: dict[int, int] = {
    1: 3,   # 22-25
    2: 5,   # 25-30
    3: 5,   # 30-35
    4: 5,   # 35-40
    5: 5,   # 40-45
    6: 5,   # 45-50
    7: 10,  # 50-60
    8: 10,  # 60-70
}

CircleType = str  # "life" | "career"


def annual_salary_for_round(age_round: int) -> int:
    """该轮在职时的年薪（第 1 轮 10 万，之后每轮 ×1.12）。"""
    exponent = max(age_round - 1, 0)
    return int(DEFAULT_ANNUAL_SALARY * (1 + SALARY_GROWTH_PER_ROUND) ** exponent)


def round_salary_income(age_round: int, employment_status: str = "employed") -> int:
    """该轮结束后累计工资 = 本轮年薪 × 本轮经过年数（仅在职发放）。"""
    from src.constants.employment import is_salary_eligible

    if not is_salary_eligible(employment_status):  # type: ignore[arg-type]
        return 0
    years = YEARS_PER_ROUND.get(age_round, 5)
    return annual_salary_for_round(age_round) * years


def get_events_per_round(age_round: int) -> int:
    return EVENTS_PER_ROUND.get(age_round, 2)


def can_pick_theme(age_round: int) -> bool:
    return age_round <= 4


def can_pick_circle_only(age_round: int) -> bool:
    return 5 <= age_round <= 7


def is_fully_random(age_round: int) -> bool:
    return age_round >= 8


def themes_for_circle(circle: CircleType) -> list[str]:
    return LIFE_THEMES if circle == "life" else CAREER_THEMES


def pick_random_theme(circle: CircleType | None = None) -> str:
    if circle == "life":
        return random.choice(LIFE_THEMES)
    if circle == "career":
        return random.choice(CAREER_THEMES)
    return random.choice(ALL_THEMES)


def pick_random_circle() -> CircleType:
    return random.choice(["life", "career"])
