from datetime import datetime, timezone
from typing import Literal
from pydantic import BaseModel, Field, field_validator

Action = Literal["GO", "AVOID", "ALTERNATIVE"]

class RecommendationRequest(BaseModel):
    city: str = Field(default="Jaipur", min_length=2, max_length=80)
    interests: list[str] = Field(default_factory=lambda: ["history", "architecture"], max_length=12)
    available_minutes: int = Field(default=240, ge=30, le=1440)
    budget_inr: int = Field(default=1000, ge=0, le=1_000_000)
    max_crowd_percent: int = Field(default=65, ge=0, le=100)
    weather: Literal["clear", "cloudy", "rain", "hot", "unknown"] = "clear"
    prefer_outdoors: bool = True

    @field_validator("interests")
    @classmethod
    def clean_interests(cls, values: list[str]) -> list[str]:
        cleaned = [v.strip().lower() for v in values if v.strip()]
        return list(dict.fromkeys(cleaned))[:12]

class Attraction(BaseModel):
    id: str
    name: str
    city: str
    description: str
    categories: list[str]
    crowd_percent: int = Field(ge=0, le=100)
    travel_minutes: int = Field(ge=0)
    visit_minutes: int = Field(ge=1)
    cost_inr: int = Field(ge=0)
    outdoors: bool
    latitude: float | None = None
    longitude: float | None = None
    data_mode: str = "simulated_demo_data"

class Recommendation(Attraction):
    action: Action
    score: float = Field(ge=0, le=100)
    reasons: list[str]

class RecommendationResponse(BaseModel):
    city: str
    data_mode: str = "simulated_demo_data"
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    recommendations: list[Recommendation]
