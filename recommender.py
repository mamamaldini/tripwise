from .data import ATTRACTIONS
from .models import Recommendation, RecommendationRequest


def _clamp(value: float, low: float = 0, high: float = 100) -> float:
    return max(low, min(high, value))


def recommend(payload: RecommendationRequest) -> list[Recommendation]:
    candidates = [a for a in ATTRACTIONS if a.city.casefold() == payload.city.casefold()]
    if not candidates:
        candidates = ATTRACTIONS
    results: list[Recommendation] = []
    for attraction in candidates:
        reasons: list[str] = []
        interest_match = len(set(payload.interests) & set(attraction.categories)) / max(1, len(set(payload.interests)))
        interest_score = interest_match * 100
        crowd_score = 100 - attraction.crowd_percent
        travel_score = _clamp(100 - attraction.travel_minutes * 1.7)
        budget_score = 100 if attraction.cost_inr <= payload.budget_inr else _clamp(100 - ((attraction.cost_inr - payload.budget_inr) / max(1, payload.budget_inr)) * 70)
        time_fit = 100 if attraction.visit_minutes + attraction.travel_minutes <= payload.available_minutes else _clamp(100 - ((attraction.visit_minutes + attraction.travel_minutes - payload.available_minutes) / payload.available_minutes) * 100)
        weather_score = 100
        if payload.weather == "rain" and attraction.outdoors:
            weather_score = 20
        elif payload.weather == "hot" and attraction.outdoors:
            weather_score = 55
        elif payload.weather == "clear" and attraction.outdoors:
            weather_score = 100
        outdoor_score = 100 if attraction.outdoors == payload.prefer_outdoors else 65
        score = round(0.28 * crowd_score + 0.22 * travel_score + 0.20 * interest_score + 0.12 * budget_score + 0.10 * time_fit + 0.05 * weather_score + 0.03 * outdoor_score, 1)

        if attraction.crowd_percent > max(payload.max_crowd_percent, 80):
            action = "AVOID"
        elif attraction.crowd_percent > payload.max_crowd_percent:
            action = "ALTERNATIVE"
        else:
            action = "GO"
        if attraction.crowd_percent <= payload.max_crowd_percent:
            reasons.append("Crowd estimate is within your preferred limit")
        else:
            reasons.append("Crowd estimate is above your preferred limit")
        if interest_match > 0:
            reasons.append("Matches your interests: " + ", ".join(sorted(set(payload.interests) & set(attraction.categories))))
        else:
            reasons.append("Limited match with selected interests")
        if attraction.travel_minutes <= 20:
            reasons.append("Relatively short estimated journey")
        if attraction.cost_inr <= payload.budget_inr:
            reasons.append("Estimated entry cost fits your budget")
        else:
            reasons.append("Estimated entry cost is above your budget")
        if payload.weather == "rain" and attraction.outdoors:
            reasons.append("Outdoor visit may be less suitable in rainy weather")
        if attraction.visit_minutes + attraction.travel_minutes > payload.available_minutes:
            reasons.append("Visit plus travel may exceed your remaining time")

        results.append(Recommendation(**attraction.model_dump(), action=action, score=score, reasons=reasons))
    return sorted(results, key=lambda item: (item.action != "GO", -item.score, item.travel_minutes))
