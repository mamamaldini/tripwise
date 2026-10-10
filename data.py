"""Seeded demo dataset. Values are illustrative, not live observations."""
from .models import Attraction

ATTRACTIONS = [
    Attraction(id="amber-fort", name="Amber Fort", city="Jaipur", description="Hilltop fort with courtyards and historic architecture.", categories=["history", "architecture", "photography"], crowd_percent=78, travel_minutes=35, visit_minutes=120, cost_inr=500, outdoors=True, latitude=26.9855, longitude=75.8513),
    Attraction(id="city-palace", name="City Palace", city="Jaipur", description="Palace complex, museums, and ornate courtyards in the old city.", categories=["history", "architecture", "culture", "photography"], crowd_percent=23, travel_minutes=18, visit_minutes=75, cost_inr=300, outdoors=False, latitude=26.9258, longitude=75.8237),
    Attraction(id="jal-mahal", name="Jal Mahal", city="Jaipur", description="Lakeside palace viewpoint, especially atmospheric near sunset.", categories=["photography", "nature", "architecture"], crowd_percent=45, travel_minutes=22, visit_minutes=35, cost_inr=0, outdoors=True, latitude=26.9535, longitude=75.8467),
    Attraction(id="hawa-mahal", name="Hawa Mahal", city="Jaipur", description="Iconic pink facade and a compact old-city visit.", categories=["history", "architecture", "photography"], crowd_percent=58, travel_minutes=12, visit_minutes=45, cost_inr=200, outdoors=True, latitude=26.9239, longitude=75.8267),
    Attraction(id="jantar-mantar", name="Jantar Mantar", city="Jaipur", description="Historic astronomical instruments and open-air heritage site.", categories=["science", "history", "architecture"], crowd_percent=34, travel_minutes=16, visit_minutes=50, cost_inr=200, outdoors=True, latitude=26.9248, longitude=75.8246),
    Attraction(id="albert-hall", name="Albert Hall Museum", city="Jaipur", description="Museum with art, artifacts, and Indo-Saracenic architecture.", categories=["museum", "history", "culture", "architecture"], crowd_percent=29, travel_minutes=20, visit_minutes=70, cost_inr=150, outdoors=False, latitude=26.9117, longitude=75.8197),
]
