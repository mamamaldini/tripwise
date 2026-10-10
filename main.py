import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from .data import ATTRACTIONS
from .models import RecommendationRequest, RecommendationResponse
from .recommender import recommend
from .integrations import gemma_summary, notify_n8n, elevenlabs_audio, get_weather

app = FastAPI(title="TripWise API", version="1.0.0", description="Explainable tourism recommendations. Demo crowd and traffic values are simulated.")
origins = [value.strip() for value in os.getenv("CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173").split(",") if value.strip()]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=False, allow_methods=["GET", "POST", "OPTIONS"], allow_headers=["Content-Type", "Authorization"])

@app.get("/api/health")
def health():
    return {"status": "ok", "service": "tripwise-api", "data_mode": "simulated_demo_data", "integrations": {"gemma_configured": bool(os.getenv("OLLAMA_BASE_URL")), "n8n_configured": bool(os.getenv("N8N_WEBHOOK_URL")), "elevenlabs_configured": bool(os.getenv("ELEVENLABS_API_KEY") and os.getenv("ELEVENLABS_VOICE_ID"))}}

@app.get("/api/attractions")
def attractions(city: str = "Jaipur"):
    matches = [a.model_dump() for a in ATTRACTIONS if a.city.casefold() == city.casefold()]
    return {"city": city, "data_mode": "simulated_demo_data", "attractions": matches or [a.model_dump() for a in ATTRACTIONS]}

@app.get("/api/weather")
async def weather(city: str = "Jaipur"):
    result = await get_weather(city)
    if result is None:
        raise HTTPException(status_code=503, detail="Weather is unavailable for this city right now. Recommendations can still run with the selected weather preference.")
    return result

@app.post("/api/recommendations", response_model=RecommendationResponse)
async def recommendations(payload: RecommendationRequest):
    ranked = recommend(payload)
    # This webhook receives only a compact summary, not a precise user location.
    await notify_n8n({"event": "recommendations_generated", "city": payload.city, "top_places": [item.name for item in ranked[:3]], "data_mode": "simulated_demo_data"})
    return RecommendationResponse(city=payload.city, recommendations=ranked)

@app.post("/api/summary")
async def summary(payload: RecommendationRequest):
    ranked = recommend(payload)
    text = await gemma_summary(payload.city, [item.name for item in ranked[:3]])
    ai_used = bool(text)
    if not text:
        top = ranked[0] if ranked else None
        text = f"For {payload.city}, start with {top.name} if it fits your plans. Crowd and travel values are demo estimates; check current local conditions before leaving." if top else "No recommendations are available for this request."
    return {"summary": text, "ai_used": ai_used, "data_mode": "simulated_demo_data"}

@app.post("/api/voice")
async def voice(payload: dict):
    text = str(payload.get("text", "")).strip()
    if not text or len(text) > 1200:
        raise HTTPException(status_code=422, detail="Provide text between 1 and 1200 characters.")
    audio = await elevenlabs_audio(text)
    if audio is None:
        raise HTTPException(status_code=503, detail="Voice integration is not configured or is temporarily unavailable.")
    return Response(content=audio, media_type="audio/mpeg", headers={"Cache-Control": "no-store"})
