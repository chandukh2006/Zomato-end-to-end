from fastapi import APIRouter, Query, HTTPException
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")


@router.get("/geocode")
async def geocode(address: str = Query(...)):
    if not GOOGLE_MAPS_API_KEY or GOOGLE_MAPS_API_KEY == "your-google-maps-api-key":
        return {
            "latitude": 28.6139,
            "longitude": 77.2090,
            "formatted_address": address
        }
    
    async with httpx.AsyncClient() as client:
        url = "https://maps.googleapis.com/maps/api/geocode/json"
        params = {
            "address": address,
            "key": GOOGLE_MAPS_API_KEY
        }
        response = await client.get(url, params=params)
        data = response.json()
        
        if data["status"] == "OK" and data["results"]:
            location = data["results"][0]["geometry"]["location"]
            return {
                "latitude": location["lat"],
                "longitude": location["lng"],
                "formatted_address": data["results"][0]["formatted_address"]
            }
        else:
            raise HTTPException(status_code=400, detail="Geocoding failed")


@router.get("/reverse")
async def reverse_geocode(lat: float = Query(...), lng: float = Query(...)):
    if not GOOGLE_MAPS_API_KEY or GOOGLE_MAPS_API_KEY == "your-google-maps-api-key":
        return {
            "formatted_address": f"Location at {lat}, {lng}",
            "city": "Delhi"
        }
    
    async with httpx.AsyncClient() as client:
        url = "https://maps.googleapis.com/maps/api/geocode/json"
        params = {
            "latlng": f"{lat},{lng}",
            "key": GOOGLE_MAPS_API_KEY
        }
        response = await client.get(url, params=params)
        data = response.json()
        
        if data["status"] == "OK" and data["results"]:
            result = data["results"][0]
            formatted_address = result["formatted_address"]
            
            city = "Unknown"
            for component in result.get("address_components", []):
                if "locality" in component.get("types", []):
                    city = component["long_name"]
                    break
                elif "administrative_area_level_1" in component.get("types", []):
                    city = component["long_name"]
            
            return {
                "formatted_address": formatted_address,
                "city": city
            }
        else:
            return {
                "formatted_address": f"Location at {lat}, {lng}",
                "city": "Unknown"
            }
