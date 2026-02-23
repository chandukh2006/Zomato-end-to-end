from fastapi import APIRouter, HTTPException
import httpx
import os
from dotenv import load_dotenv

load_dotenv()
router = APIRouter()

GOOGLE_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

@router.get("/reverse")
async def reverse_geocode(lat: float, lng: float):
    if not GOOGLE_API_KEY or GOOGLE_API_KEY == "your-google-maps-api-key":
        # Return a dummy address if no API key
        return {"address": f"Location ({round(lat,4)}, {round(lng,4)})"}
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://maps.googleapis.com/maps/api/geocode/json",
                params={"latlng": f"{lat},{lng}", "key": GOOGLE_API_KEY}
            )
            data = response.json()
        if data["status"] == "OK":
            return {"address": data["results"][0]["formatted_address"]}
        return {"address": f"Location ({round(lat,4)}, {round(lng,4)})"}
    except:
        return {"address": f"Location ({round(lat,4)}, {round(lng,4)})"}

@router.get("/geocode")
async def geocode_address(address: str):
    if not GOOGLE_API_KEY or GOOGLE_API_KEY == "your-google-maps-api-key":
        return {"lat": 28.6139, "lng": 77.2090, "formatted_address": address}
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://maps.googleapis.com/maps/api/geocode/json",
                params={"address": address, "key": GOOGLE_API_KEY}
            )
            data = response.json()
        if data["status"] == "OK":
            loc = data["results"][0]["geometry"]["location"]
            return {"lat": loc["lat"], "lng": loc["lng"], "formatted_address": data["results"][0]["formatted_address"]}
        return {"lat": 28.6139, "lng": 77.2090, "formatted_address": address}
    except:
        return {"lat": 28.6139, "lng": 77.2090, "formatted_address": address}
