from .models import RecommendationRequest
from .recommender import recommend


def test_recommendations_are_sorted_and_bounded():
    result = recommend(RecommendationRequest(city="Jaipur", interests=["history"], available_minutes=240, budget_inr=1000, max_crowd_percent=65))
    assert result
    assert all(0 <= item.score <= 100 for item in result)
    assert result[0].score >= result[-1].score or result[0].action == "GO"


def test_unknown_city_falls_back_to_demo_dataset():
    result = recommend(RecommendationRequest(city="Somewhere", interests=["nature"]))
    assert len(result) > 0


def test_rain_reasons_flag_outdoor_places():
    result = recommend(RecommendationRequest(city="Jaipur", weather="rain", prefer_outdoors=False))
    outdoor = next(item for item in result if item.outdoors)
    assert any("rainy weather" in reason for reason in outdoor.reasons)
