"""游戏相关 Pydantic 模型。"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class CreateGameRequest(BaseModel):
    """创建游戏请求（角色姓名仅存前端 localStorage）。"""

    model_config = ConfigDict(extra="ignore")

    money: int = Field(default=50000, ge=0)
    energy: int = Field(default=10, ge=0)
    joy: int = Field(default=0, ge=0)


class GamePublic(BaseModel):
    id: int
    user_id: int
    status: str
    age_round: int
    age_range: str
    money: int
    energy: int
    joy: int
    employment_status: str = "employed"
    decisions: list
    ai_review: str | None
    created_at: str
    updated_at: str


class DrawEventRequest(BaseModel):
    model_config = ConfigDict(extra="ignore")

    circle: str | None = None
    theme: str | None = None


class EventOptionPublic(BaseModel):
    option_id: str
    text: str
    money_change: int
    energy_change: int
    joy_change: int


class GameEventPublic(BaseModel):
    event_id: str
    title: str
    description: str
    options: list[EventOptionPublic]


class DrawEventResponse(BaseModel):
    events: list[GameEventPublic]
    count: int


class ChoiceRequest(BaseModel):
    """提交决策请求。"""

    model_config = ConfigDict(extra="ignore")

    event_id: str
    option_id: str
    circle: str
    theme: str
    event_title: str
    event_description: str
    chosen_option_text: str
    money_change: int = 0
    energy_change: int = 0
    joy_change: int = 0


class DecisionPublic(BaseModel):
    round: int
    age_range: str
    circle: str
    theme: str
    event_title: str
    event_description: str
    chosen_option: str
    money_change: int
    energy_change: int
    joy_change: int


class ChoiceResponse(GamePublic):
    last_decision: DecisionPublic


class AdvanceRoundResponse(GamePublic):
    round_salary_income: int = 0
    annual_salary: int = 0


class FinishResultPublic(BaseModel):
    id: int
    outcome_tags: list[str]
    money: int
    energy: int
    joy: int
    ai_review: str
    decisions: list
