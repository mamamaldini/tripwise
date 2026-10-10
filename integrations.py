"""Optional integrations. Keep credentials server-side and fail gracefully."""
import os
import httpx

async def gemma_summary(city: str, names: list[str]) -> str | None:
    base = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434").rstrip("/")
    model = os.getenv("OLLAMA_MODEL", "gemma3:4b")
    prompt = f"Give a concise, cautious travel recommendation for {city}. Candidate places: {', '.join(names)}. Do not invent live conditions; mention that crowd values are demo estimates. Under 60 words."
    try:
        async with httpx.AsyncClient(timeout=8.0) as client:
            response = await client.post(f"{base}/api/generate", json={"model": model, "prompt": prompt, "stream": False})
            response.raise_for_status()
            body = response.json()
            return body.get("response", "").strip() or None
    except (httpx.HTTPError, ValueError):
        return None

async def notify_n8n(payload: dict) -> bool:
    url = os.getenv("N8N_WEBHOOK_URL", "").strip()
    if not url:
        return False
    try:
        async with httpx.AsyncClient(timeout=4.0) as client:
            response = await client.post(url, json=payload)
            response.raise_for_status()
            return True
    except httpx.HTTPError:
        return False

async def elevenlabs_audio(text: str) -> bytes | None:
    api_key = os.getenv("ELEVENLABS_API_KEY", "").strip()
    voice_id = os.getenv("ELEVENLABS_VOICE_ID", "").strip()
    if not api_key or not voice_id:
        return None
    model_id = os.getenv("ELEVENLABS_MODEL_ID", "eleven_multilingual_v2")
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    try:
        async with httpx.AsyncClient(timeout=20.0) as client:
            response = await client.post(url, headers={"xi-api-key": api_key, "Accept": "audio/mpeg", "Content-Type": "application/json"}, json={"text": text[:1200], "model_id": model_id})
            response.raise_for_status()
            return response.content
    except httpx.HTTPError:
        return None

async def get_weather(city: str) -> dict | None:
    """Fetch current weather from Open-Meteo for supported demo cities."""
    coordinates = {
        "jaipur": (26.9124, 75.7873),
        "delhi": (28.6139, 77.2090),
        "mumbai": (19.0760, 72.8777),
        "goa": (15.2993, 74.1240),
        "agra": (27.1767, 78.0081),
    }
    coords = coordinates.get(city.strip().casefold())
    if not coords:
        return None
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get("https://api.open-meteo.com/v1/forecast", params={"latitude": coords[0], "longitude": coords[1], "current": "temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,weather_code,wind_speed_10m", "timezone": "auto"})
            response.raise_for_status()
            data = response.json()
            current = data.get("current")
            if not isinstance(current, dict):
                return None
            return {"city": city, "provider": "Open-Meteo", "observed_at": current.get("time"), "temperature_c": current.get("temperature_2m"), "feels_like_c": current.get("apparent_temperature"), "humidity_percent": current.get("relative_humidity_2m"), "precipitation_mm": current.get("precipitation"), "weather_code": current.get("weather_code"), "wind_speed_kmh": current.get("wind_speed_10m"), "data_mode": "provider_current_weather"}
    except (httpx.HTTPError, ValueError):
        return None
