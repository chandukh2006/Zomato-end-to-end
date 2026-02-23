from fastapi import APIRouter, Query, HTTPException
from typing import Optional
import math
from app.models import Restaurant, MenuItem

router = APIRouter()

def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    return R * 2 * math.asin(math.sqrt(a))

@router.get("/restaurants")
async def get_restaurants(lat=None, lng=None, filter=None):
    query = {"is_open": True}
    if filter == "veg":
        query["tags"] = {"$in": ["veg"]}
    elif filter == "fast":
        query["delivery_time_mins"] = {"$lt": 30}
    elif filter == "top":
        query["rating"] = {"$gte": 4.0}
    restaurants = await Restaurant.find(query).to_list()
    result = []
    for r in restaurants:
        r_dict = r.dict()
        r_dict["_id"] = str(r.id)
        r_dict["distance"] = round(haversine_distance(lat, lng, r.latitude, r.longitude), 2) if lat and lng else None
        result.append(r_dict)
    if lat and lng:
        result.sort(key=lambda x: x["distance"])
    return result

@router.get("/restaurants/{restaurant_id}")
async def get_restaurant(restaurant_id: str):
    restaurant = await Restaurant.get(restaurant_id)
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    result = restaurant.dict()
    result["_id"] = str(restaurant.id)
    return result

@router.get("/restaurants/{restaurant_id}/items")
async def get_menu_items(restaurant_id: str):
    items = await MenuItem.find({"restaurant_id": restaurant_id, "is_available": True}).to_list()
    grouped = {}
    for item in items:
        cat = item.category
        if cat not in grouped:
            grouped[cat] = []
        d = item.dict()
        d["_id"] = str(item.id)
        grouped[cat].append(d)
    return grouped

@router.get("/search")
async def search_menu_items(q: str):
    items = await MenuItem.find({"name": {"$regex": q, "$options": "i"}, "is_available": True}).to_list()
    result = []
    for item in items:
        d = item.dict()
        d["_id"] = str(item.id)
        r = await Restaurant.get(item.restaurant_id)
        if r:
            d["restaurant_name"] = r.name
            d["restaurant_id"] = str(r.id)
        result.append(d)
    return result
