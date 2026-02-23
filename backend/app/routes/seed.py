from fastapi import APIRouter
from app.models import Restaurant, MenuItem
from datetime import datetime

router = APIRouter()

@router.post("")
async def seed_database():
    """Seed database with sample restaurants and menu items"""
    # Clear existing data
    await Restaurant.find_all().delete()
    await MenuItem.find_all().delete()
    
    # Sample restaurants
    restaurants_data = [
        {
            "name": "Spice Garden",
            "cuisine_type": "North Indian",
            "rating": 4.5,
            "delivery_time_mins": 25,
            "min_order": 150.0,
            "latitude": 28.6139,
            "longitude": 77.2090,
            "address": "Connaught Place, New Delhi",
            "image_url": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=800",
            "is_open": True,
            "tags": ["veg", "fast", "trending"]
        },
        {
            "name": "Burger King",
            "cuisine_type": "Fast Food",
            "rating": 4.2,
            "delivery_time_mins": 20,
            "min_order": 100.0,
            "latitude": 28.5355,
            "longitude": 77.3910,
            "address": "Gurgaon Sector 29",
            "image_url": "https://images.unsplash.com/photo-1571091718767-18b5b1457add?w=800",
            "is_open": True,
            "tags": ["fast", "trending"]
        },
        {
            "name": "Pizza Hut",
            "cuisine_type": "Italian",
            "rating": 4.0,
            "delivery_time_mins": 30,
            "min_order": 200.0,
            "latitude": 28.7041,
            "longitude": 77.1025,
            "address": "Saket, New Delhi",
            "image_url": "https://images.unsplash.com/photo-1513104890138-7c749659a591?w=800",
            "is_open": True,
            "tags": ["veg", "trending"]
        },
        {
            "name": "Sushi Express",
            "cuisine_type": "Japanese",
            "rating": 4.7,
            "delivery_time_mins": 35,
            "min_order": 300.0,
            "latitude": 28.5562,
            "longitude": 77.1000,
            "address": "Vasant Kunj, New Delhi",
            "image_url": "https://images.unsplash.com/photo-1579584425555-c3ce17fd4351?w=800",
            "is_open": True,
            "tags": ["top"]
        },
        {
            "name": "Taco Bell",
            "cuisine_type": "Mexican",
            "rating": 4.1,
            "delivery_time_mins": 22,
            "min_order": 120.0,
            "latitude": 28.4089,
            "longitude": 77.0378,
            "address": "Dwarka, New Delhi",
            "image_url": "https://images.unsplash.com/photo-1565299585323-38174c0b5c3a?w=800",
            "is_open": True,
            "tags": ["fast"]
        },
        {
            "name": "Green Leaf",
            "cuisine_type": "Vegetarian",
            "rating": 4.3,
            "delivery_time_mins": 28,
            "min_order": 180.0,
            "latitude": 28.6278,
            "longitude": 77.2066,
            "address": "Karol Bagh, New Delhi",
            "image_url": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=800",
            "is_open": True,
            "tags": ["veg", "top"]
        }
    ]
    
    restaurants = []
    for r_data in restaurants_data:
        restaurant = Restaurant(**r_data)
        await restaurant.insert()
        restaurants.append(restaurant)
    
    # Sample menu items
    menu_items_data = [
        # Spice Garden
        {"restaurant_id": str(restaurants[0].id), "name": "Butter Chicken", "description": "Creamy tomato-based curry with tender chicken pieces", "price": 280.0, "category": "Main Course", "is_veg": False, "is_available": True, "image_url": "https://images.unsplash.com/photo-1603133872878-684f208fb84b?w=400"},
        {"restaurant_id": str(restaurants[0].id), "name": "Dal Makhani", "description": "Creamy black lentils cooked overnight", "price": 180.0, "category": "Main Course", "is_veg": True, "is_available": True, "image_url": "https://images.unsplash.com/photo-1585937421612-70a008356fbe?w=400"},
        {"restaurant_id": str(restaurants[0].id), "name": "Garlic Naan", "description": "Fresh baked bread with garlic butter", "price": 60.0, "category": "Bread", "is_veg": True, "is_available": True, "image_url": "https://images.unsplash.com/photo-1509440159596-0249088772ff?w=400"},
        {"restaurant_id": str(restaurants[0].id), "name": "Paneer Tikka", "description": "Grilled cottage cheese with spices", "price": 220.0, "category": "Appetizer", "is_veg": True, "is_available": True, "image_url": "https://images.unsplash.com/photo-1601050690597-df0568f70950?w=400"},
        
        # Burger King
        {"restaurant_id": str(restaurants[1].id), "name": "Whopper", "description": "Flame-grilled beef patty with fresh veggies", "price": 199.0, "category": "Burgers", "is_veg": False, "is_available": True, "image_url": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=400"},
        {"restaurant_id": str(restaurants[1].id), "name": "Veg Whopper", "description": "Plant-based patty with fresh veggies", "price": 179.0, "category": "Burgers", "is_veg": True, "is_available": True, "image_url": "https://images.unsplash.com/photo-1525059696034-4967a7290022?w=400"},
        {"restaurant_id": str(restaurants[1].id), "name": "French Fries", "description": "Crispy golden fries", "price": 99.0, "category": "Sides", "is_veg": True, "is_available": True, "image_url": "https://images.unsplash.com/photo-1573080496219-bb080dd4f877?w=400"},
        {"restaurant_id": str(restaurants[1].id), "name": "Chicken Nuggets", "description": "6 pieces of crispy chicken nuggets", "price": 149.0, "category": "Sides", "is_veg": False, "is_available": True, "image_url": "https://images.unsplash.com/photo-1626082927389-6cd097cdc6ec?w=400"},
        
        # Pizza Hut
        {"restaurant_id": str(restaurants[2].id), "name": "Margherita", "description": "Classic tomato, mozzarella, and basil", "price": 299.0, "category": "Pizza", "is_veg": True, "is_available": True, "image_url": "https://images.unsplash.com/photo-1574071318508-1cdbab80d002?w=400"},
        {"restaurant_id": str(restaurants[2].id), "name": "Pepperoni", "description": "Spicy pepperoni with mozzarella", "price": 399.0, "category": "Pizza", "is_veg": False, "is_available": True, "image_url": "https://images.unsplash.com/photo-1628840042765-356cda07504e?w=400"},
        {"restaurant_id": str(restaurants[2].id), "name": "Garlic Bread", "description": "Buttery garlic bread sticks", "price": 149.0, "category": "Sides", "is_veg": True, "is_available": True, "image_url": "https://images.unsplash.com/photo-1509440159596-0249088772ff?w=400"},
        
        # Sushi Express
        {"restaurant_id": str(restaurants[3].id), "name": "Salmon Sashimi", "description": "Fresh salmon slices", "price": 450.0, "category": "Sashimi", "is_veg": False, "is_available": True, "image_url": "https://images.unsplash.com/photo-1579584425555-c3ce17fd4351?w=400"},
        {"restaurant_id": str(restaurants[3].id), "name": "California Roll", "description": "Crab, avocado, cucumber", "price": 320.0, "category": "Rolls", "is_veg": False, "is_available": True, "image_url": "https://images.unsplash.com/photo-1579584425555-c3ce17fd4351?w=400"},
        {"restaurant_id": str(restaurants[3].id), "name": "Miso Soup", "description": "Traditional Japanese soup", "price": 150.0, "category": "Soup", "is_veg": True, "is_available": True, "image_url": "https://images.unsplash.com/photo-1547592166-23ac45744acd?w=400"},
        
        # Taco Bell
        {"restaurant_id": str(restaurants[4].id), "name": "Crunchy Taco", "description": "Crispy shell with seasoned beef", "price": 99.0, "category": "Tacos", "is_veg": False, "is_available": True, "image_url": "https://images.unsplash.com/photo-1565299585323-38174c0b5c3a?w=400"},
        {"restaurant_id": str(restaurants[4].id), "name": "Veg Crunchy Taco", "description": "Crispy shell with beans and veggies", "price": 89.0, "category": "Tacos", "is_veg": True, "is_available": True, "image_url": "https://images.unsplash.com/photo-1565299585323-38174c0b5c3a?w=400"},
        {"restaurant_id": str(restaurants[4].id), "name": "Nachos Supreme", "description": "Loaded nachos with cheese and jalapeños", "price": 199.0, "category": "Sides", "is_veg": True, "is_available": True, "image_url": "https://images.unsplash.com/photo-1513456855341-7aa18d8c8f3a?w=400"},
        
        # Green Leaf
        {"restaurant_id": str(restaurants[5].id), "name": "Veg Thali", "description": "Complete meal with 4 curries, rice, roti", "price": 250.0, "category": "Thali", "is_veg": True, "is_available": True, "image_url": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=400"},
        {"restaurant_id": str(restaurants[5].id), "name": "Palak Paneer", "description": "Spinach curry with cottage cheese", "price": 200.0, "category": "Main Course", "is_veg": True, "is_available": True, "image_url": "https://images.unsplash.com/photo-1585937421612-70a008356fbe?w=400"},
        {"restaurant_id": str(restaurants[5].id), "name": "Gulab Jamun", "description": "Sweet milk dumplings in syrup", "price": 80.0, "category": "Dessert", "is_veg": True, "is_available": True, "image_url": "https://images.unsplash.com/photo-1606313564200-e75d5e30476c?w=400"},
    ]
    
    for item_data in menu_items_data:
        menu_item = MenuItem(**item_data)
        await menu_item.insert()
    
    return {
        "message": "Database seeded successfully",
        "restaurants": len(restaurants),
        "menu_items": len(menu_items_data)
    }
