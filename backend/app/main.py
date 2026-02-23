from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
import os
from dotenv import load_dotenv

from app.models import User, Restaurant, MenuItem, CartItem, Order
from app.routes import auth, menu, cart, orders, geo, seed

load_dotenv()

app = FastAPI(title="Zomato API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def init_db():
    """Initialize MongoDB connection and Beanie"""
    mongodb_url = os.getenv("MONGODB_URL", "mongodb://localhost:27017/zomato_db")
    client = AsyncIOMotorClient(mongodb_url)
    database = client.get_database("zomato_db")
    
    await init_beanie(
        database=database,
        document_models=[User, Restaurant, MenuItem, CartItem, Order]
    )
    print("✅ Database connected")

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(menu.router, prefix="/menu", tags=["menu"])
app.include_router(cart.router, prefix="/cart", tags=["cart"])
app.include_router(orders.router, prefix="/orders", tags=["orders"])
app.include_router(geo.router, prefix="/geo", tags=["geo"])
app.include_router(seed.router, prefix="/seed", tags=["seed"])

@app.get("/")
async def root():
    return {"message": "Zomato API is running"}
