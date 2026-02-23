from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from app.models import User

load_dotenv()

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-minimum-32-chars")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str
    phone: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class RegisterResponse(BaseModel):
    user_id: str
    message: str


class LoginResponse(BaseModel):
    token: str
    user_id: str
    name: str


@router.post("/register", response_model=RegisterResponse)
async def register(request: RegisterRequest):
    existing_user = await User.find_one(User.email == request.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    password_hash = get_password_hash(request.password)
    user = User(
        name=request.name,
        email=request.email,
        password_hash=password_hash,
        phone=request.phone,
        address="",
        latitude=0.0,
        longitude=0.0
    )
    await user.insert()
    return RegisterResponse(user_id=str(user.id), message="User registered successfully")


@router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest):
    user = await User.find_one(User.email == request.email)
    if not user or not verify_password(request.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    token = create_access_token(data={"sub": str(user.id), "email": user.email})
    return LoginResponse(
        token=token,
        user_id=str(user.id),
        name=user.name
    )
