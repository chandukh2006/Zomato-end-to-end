from beanie import Document
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List, Optional
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

class User(Document):
    name: str
    email: EmailStr
    password_hash: str
    phone: str
    address: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    created_at: datetime = datetime.utcnow()

    class Settings:
        name = "users"
        indexes = ["email"]

class Restaurant(Document):
    name: str
    cuisine_type: str
    rating: float
    delivery_time_mins: int
    min_order: float
    latitude: float
    longitude: float
    address: str
    image_url: str
    is_open: bool
    tags: List[str] = []

    class Settings:
        name = "restaurants"

class MenuItem(Document):
    restaurant_id: str
    name: str
    description: str
    price: float
    category: str
    is_veg: bool
    is_available: bool
    image_url: str

    class Settings:
        name = "menu_items"

class CartItem(Document):
    user_id: str
    menu_item_id: str
    restaurant_id: str
    quantity: int

    class Settings:
        name = "cart_items"

class OrderItem(BaseModel):
    menu_item_id: str
    name: str
    quantity: int
    unit_price: float

class Order(Document):
    user_id: str
    restaurant_id: str
    status: str  # pending|confirmed|preparing|out_for_delivery|delivered|cancelled
    total_amount: float
    delivery_address: str
    delivery_lat: float
    delivery_lng: float
    items: List[OrderItem]
    created_at: datetime = datetime.utcnow()

    class Settings:
        name = "orders"
