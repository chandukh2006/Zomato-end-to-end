from fastapi import APIRouter, Query, HTTPException
from typing import Optional, List
from app.models import Restaurant, MenuItem
import math

router = APIRouter()


def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    return R * c


@router.get("/restaurants")
async def get_restaurants(
    lat: Optional[float] = Query(None),
    lng: Optional[float] = Query(None),
    filter: Optional[str] = Query(None)
):
    restaurants = await Restaurant.find(Restaurant.is_open == True).to_list()
    
    if filter == "veg":
        restaurants = [r for r in restaurants if "veg" in r.tags]
    elif filter == "fast":
        restaurants = [r for r in restaurants if r.delivery_time_mins < 30]
    elif filter == "top":
        restaurants = [r for r in restaurants if r.rating >= 4.0]
    
    if lat and lng:
        for r in restaurants:
            r.distance = haversine_distance(lat, lng, r.latitude, r.longitude)
        restaurants.sort(key=lambda x: x.distance)
    else:
        for r in restaurants:
            r.distance = None
    
    return [
        {
            "_id": str(r.id),
            "name": r.name,
            "cuisine_type": r.cuisine_type,
            "rating": r.rating,
            "delivery_time_mins": r.delivery_time_mins,
            "min_order": r.min_order,
            "latitude": r.latitude,
            "longitude": r.longitude,
            "address": r.address,
            "image_url": r.image_url,
            "is_open": r.is_open,
            "tags": r.tags,
            "distance": r.distance
        }
        for r in restaurants
    ]


@router.get("/restaurants/{restaurant_id}")
async def get_restaurant(restaurant_id: str):
    restaurant = await Restaurant.get(restaurant_id)
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return {
        "_id": str(restaurant.id),
        "name": restaurant.name,
        "cuisine_type": restaurant.cuisine_type,
        "rating": restaurant.rating,
        "delivery_time_mins": restaurant.delivery_time_mins,
        "min_order": restaurant.min_order,
        "latitude": restaurant.latitude,
        "longitude": restaurant.longitude,
        "address": restaurant.address,
        "image_url": restaurant.image_url,
        "is_open": restaurant.is_open,
        "tags": restaurant.tags
    }


@router.get("/restaurants/{restaurant_id}/items")
async def get_menu_items(restaurant_id: str):
    items = await MenuItem.find(MenuItem.restaurant_id == restaurant_id).to_list()
    
    grouped = {}
    for item in items:
        if item.category not in grouped:
            grouped[item.category] = []
        grouped[item.category].append({
            "_id": str(item.id),
            "restaurant_id": item.restaurant_id,
            "name": item.name,
            "description": item.description,
            "price": item.price,
            "category": item.category,
            "is_veg": item.is_veg,
            "is_available": item.is_available,
            "image_url": item.image_url
        })
    
    return grouped


@router.get("/search")
async def search_menu_items(q: str = Query(...)):
    items = await MenuItem.find({
        "$or": [
            {"name": {"$regex": q, "$options": "i"}},
            {"description": {"$regex": q, "$options": "i"}}
        ]
    }).to_list()
    
    restaurants_dict = {}
    for item in items:
        if item.restaurant_id not in restaurants_dict:
            restaurant = await Restaurant.get(item.restaurant_id)
            if restaurant:
                restaurants_dict[item.restaurant_id] = {
                    "_id": str(restaurant.id),
                    "name": restaurant.name,
                    "image_url": restaurant.image_url,
                    "rating": restaurant.rating,
                    "delivery_time_mins": restaurant.delivery_time_mins
                }
    
    return {
        "items": [
            {
                "_id": str(item.id),
                "restaurant_id": item.restaurant_id,
                "name": item.name,
                "description": item.description,
                "price": item.price,
                "category": item.category,
                "is_veg": item.is_veg,
                "is_available": item.is_available,
                "image_url": item.image_url,
                "restaurant": restaurants_dict.get(item.restaurant_id)
            }
            for item in items
        ]
    }
