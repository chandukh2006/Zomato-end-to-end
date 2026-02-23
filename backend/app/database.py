from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.models import User, Restaurant, MenuItem, CartItem, Order
import os
from dotenv import load_dotenv

load_dotenv()

client = None
database = None


async def init_db():
    global client, database
    mongodb_url = os.getenv("MONGODB_URL", "mongodb://localhost:27017/zomato_db")
    client = AsyncIOMotorClient(mongodb_url)
    database = client.get_database("zomato_db")
    
    await init_beanie(
        database=database,
        document_models=[User, Restaurant, MenuItem, CartItem, Order]
    )
