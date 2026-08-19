"""就业状态与事件选择绑定（影响轮次工资）。"""

from __future__ import annotations

from typing import Literal

EmploymentStatus = Literal["employed", "entrepreneur", "unemployed"]

# 子主题为「创业」→ 无固定工资
NO_SALARY_THEMES: frozenset[str] = frozenset({"创业"})

# 子主题为「工作」且选项未明确离职/创业 → 视为在职
EMPLOYED_THEMES: frozenset[str] = frozenset({"工作"})

ENTREPRENEUR_HINTS: tuple[str, ...] = (
    "创业",
    "开店",
    "开公司",
    "自立门户",
    "全职创业",
    "当老板",
    "自己当老板",
    "辞职创业",
)

UNEMPLOYED_HINTS: tuple[str, ...] = (
    "辞职",
    "离职",
    "裸辞",
    "失业",
    "被裁",
    "裁员",
    "待业",
    "不干了",
    "关停",
    "破产",
    "躺平",
    "休息一阵",
)

REEMPLOY_HINTS: tuple[str, ...] = (
    "入职",
    "重返职场",
    "重新工作",
    "找到新工作",
    "回去上班",
    "继续上班",
    "重返岗位",
    "接受offer",
    "接受 offer",
    "接受这份",
    "留任",
    "晋升",
    "坚守岗位",
    "认真工作",
)


def _contains_any(text: str, hints: tuple[str, ...]) -> bool:
    lowered = text.lower()
    return any(hint.lower() in lowered for hint in hints)


def resolve_employment_status(
    *,
    current: EmploymentStatus,
    theme: str,
    event_title: str,
    event_description: str,
    chosen_option: str,
) -> EmploymentStatus:
    """根据所选选项与子主题更新就业状态（仅看玩家选择，不看事件描述文案）。"""
    del event_title, event_description  # 事件背景不参与判定，避免「裁员/辞职」等描述误触发

    if theme in NO_SALARY_THEMES:
        return "entrepreneur"

    if _contains_any(chosen_option, UNEMPLOYED_HINTS):
        return "unemployed"

    if _contains_any(chosen_option, ENTREPRENEUR_HINTS):
        return "entrepreneur"

    if _contains_any(chosen_option, REEMPLOY_HINTS):
        return "employed"

    if theme in EMPLOYED_THEMES:
        return "employed"

    return current


def is_salary_eligible(status: EmploymentStatus) -> bool:
    return status == "employed"
