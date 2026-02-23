from fastapi import APIRouter
from app.models import Restaurant, MenuItem
from datetime import datetime

router = APIRouter()


@router.post("")
async def seed_database():
    await Restaurant.delete_all()
    await MenuItem.delete_all()
    
    restaurants_data = [
        {
            "name": "Biryani House",
            "cuisine_type": "Indian",
            "rating": 4.5,
            "delivery_time_mins": 25,
            "min_order": 200.0,
            "latitude": 28.6139,
            "longitude": 77.2090,
            "address": "123 Main Street, Delhi",
            "image_url": "https://images.unsplash.com/photo-1585937421612-70a008356fbe?w=800",
            "is_open": True,
            "tags": ["non-veg", "trending"]
        },
        {
            "name": "Green Leaf Cafe",
            "cuisine_type": "Vegetarian",
            "rating": 4.2,
            "delivery_time_mins": 20,
            "min_order": 150.0,
            "latitude": 28.6140,
            "longitude": 77.2091,
            "address": "456 Park Avenue, Delhi",
            "image_url": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=800",
            "is_open": True,
            "tags": ["veg", "fast"]
        },
        {
            "name": "Pizza Paradise",
            "cuisine_type": "Italian",
            "rating": 4.7,
            "delivery_time_mins": 30,
            "min_order": 300.0,
            "latitude": 28.6141,
            "longitude": 77.2092,
            "address": "789 Food Street, Delhi",
            "image_url": "https://images.unsplash.com/photo-1513104890138-7c749659a591?w=800",
            "is_open": True,
            "tags": ["non-veg", "top"]
        },
        {
            "name": "Sushi Express",
            "cuisine_type": "Japanese",
            "rating": 4.3,
            "delivery_time_mins": 35,
            "min_order": 400.0,
            "latitude": 28.6142,
            "longitude": 77.2093,
            "address": "321 Market Road, Delhi",
            "image_url": "https://images.unsplash.com/photo-1579584425555-c3ce17fd4351?w=800",
            "is_open": True,
            "tags": ["non-veg"]
        },
        {
            "name": "Taco Fiesta",
            "cuisine_type": "Mexican",
            "rating": 4.0,
            "delivery_time_mins": 22,
            "min_order": 250.0,
            "latitude": 28.6143,
            "longitude": 77.2094,
            "address": "654 Spice Lane, Delhi",
            "image_url": "https://images.unsplash.com/photo-1565299585323-38174c0c0e5c?w=800",
            "is_open": True,
            "tags": ["veg", "fast"]
        },
        {
            "name": "Burger Junction",
            "cuisine_type": "American",
            "rating": 4.4,
            "delivery_time_mins": 18,
            "min_order": 180.0,
            "latitude": 28.6144,
            "longitude": 77.2095,
            "address": "987 Burger Street, Delhi",
            "image_url": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=800",
            "is_open": True,
            "tags": ["non-veg", "fast", "trending"]
        }
    ]
    
    restaurants = []
    for r_data in restaurants_data:
        restaurant = Restaurant(**r_data)
        await restaurant.insert()
        restaurants.append(restaurant)
    
    menu_items_data = [
        {
            "restaurant_id": str(restaurants[0].id),
            "name": "Chicken Biryani",
            "description": "Fragrant basmati rice cooked with tender chicken pieces and aromatic spices",
            "price": 250.0,
            "category": "Main Course",
            "is_veg": False,
            "is_available": True,
            "image_url": "https://images.unsplash.com/photo-1585937421612-70a008356fbe?w=400"
        },
        {
            "restaurant_id": str(restaurants[0].id),
            "name": "Mutton Biryani",
            "description": "Rich and flavorful mutton biryani with perfectly cooked meat",
            "price": 350.0,
            "category": "Main Course",
            "is_veg": False,
            "is_available": True,
            "image_url": "https://images.unsplash.com/photo-1585937421612-70a008356fbe?w=400"
        },
        {
            "restaurant_id": str(restaurants[0].id),
            "name": "Raita",
            "description": "Cool and refreshing yogurt side dish",
            "price": 50.0,
            "category": "Sides",
            "is_veg": True,
            "is_available": True,
            "image_url": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=400"
        },
        {
            "restaurant_id": str(restaurants[1].id),
            "name": "Paneer Tikka",
            "description": "Grilled cottage cheese marinated in spices",
            "price": 180.0,
            "category": "Starters",
            "is_veg": True,
            "is_available": True,
            "image_url": "https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=400"
        },
        {
            "restaurant_id": str(restaurants[1].id),
            "name": "Dal Makhani",
            "description": "Creamy black lentils cooked to perfection",
            "price": 150.0,
            "category": "Main Course",
            "is_veg": True,
            "is_available": True,
            "image_url": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=400"
        },
        {
            "restaurant_id": str(restaurants[1].id),
            "name": "Naan",
            "description": "Freshly baked soft bread",
            "price": 40.0,
            "category": "Breads",
            "is_veg": True,
            "is_available": True,
            "image_url": "https://images.unsplash.com/photo-1509440159596-0249088772ff?w=400"
        },
        {
            "restaurant_id": str(restaurants[2].id),
            "name": "Margherita Pizza",
            "description": "Classic pizza with tomato, mozzarella, and basil",
            "price": 350.0,
            "category": "Pizzas",
            "is_veg": True,
            "is_available": True,
            "image_url": "https://images.unsplash.com/photo-1574071318508-1cdbab80d002?w=400"
        },
        {
            "restaurant_id": str(restaurants[2].id),
            "name": "Pepperoni Pizza",
            "description": "Spicy pepperoni with mozzarella cheese",
            "price": 450.0,
            "category": "Pizzas",
            "is_veg": False,
            "is_available": True,
            "image_url": "https://images.unsplash.com/photo-1574071318508-1cdbab80d002?w=400"
        },
        {
            "restaurant_id": str(restaurants[2].id),
            "name": "Garlic Bread",
            "description": "Crispy bread with garlic butter",
            "price": 120.0,
            "category": "Sides",
            "is_veg": True,
            "is_available": True,
            "image_url": "https://images.unsplash.com/photo-1509440159596-0249088772ff?w=400"
        },
        {
            "restaurant_id": str(restaurants[3].id),
            "name": "Salmon Sushi Roll",
            "description": "Fresh salmon with avocado and cucumber",
            "price": 500.0,
            "category": "Sushi",
            "is_veg": False,
            "is_available": True,
            "image_url": "https://images.unsplash.com/photo-1579584425555-c3ce17fd4351?w=400"
        },
        {
            "restaurant_id": str(restaurants[3].id),
            "name": "California Roll",
            "description": "Crab, avocado, and cucumber roll",
            "price": 350.0,
            "category": "Sushi",
            "is_veg": False,
            "is_available": True,
            "image_url": "https://images.unsplash.com/photo-1579584425555-c3ce17fd4351?w=400"
        },
        {
            "restaurant_id": str(restaurants[4].id),
            "name": "Veggie Tacos",
            "description": "Soft tortillas filled with fresh vegetables",
            "price": 200.0,
            "category": "Tacos",
            "is_veg": True,
            "is_available": True,
            "image_url": "https://images.unsplash.com/photo-1565299585323-38174c0c0e5c?w=400"
        },
        {
            "restaurant_id": str(restaurants[4].id),
            "name": "Chicken Tacos",
            "description": "Spiced chicken in soft tortillas",
            "price": 250.0,
            "category": "Tacos",
            "is_veg": False,
            "is_available": True,
            "image_url": "https://images.unsplash.com/photo-1565299585323-38174c0c0e5c?w=400"
        },
        {
            "restaurant_id": str(restaurants[5].id),
            "name": "Classic Burger",
            "description": "Juicy beef patty with fresh vegetables",
            "price": 200.0,
            "category": "Burgers",
            "is_veg": False,
            "is_available": True,
            "image_url": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=400"
        },
        {
            "restaurant_id": str(restaurants[5].id),
            "name": "Veggie Burger",
            "description": "Plant-based patty with all the fixings",
            "price": 180.0,
            "category": "Burgers",
            "is_veg": True,
            "is_available": True,
            "image_url": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=400"
        },
        {
            "restaurant_id": str(restaurants[5].id),
            "name": "French Fries",
            "description": "Crispy golden fries",
            "price": 80.0,
            "category": "Sides",
            "is_veg": True,
            "is_available": True,
            "image_url": "https://images.unsplash.com/photo-1573080496219-bb080dd4f877?w=400"
        }
    ]
    
    for item_data in menu_items_data:
        menu_item = MenuItem(**item_data)
        await menu_item.insert()
    
    return {
        "message": "Database seeded successfully",
        "restaurants": len(restaurants),
        "menu_items": len(menu_items_data)
    }
