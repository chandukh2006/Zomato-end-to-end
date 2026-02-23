# Quick Start Guide

## 🚀 How to Run the Application

### Step 1: Start MongoDB
Make sure MongoDB is running on your system:
- **Local MongoDB**: Ensure it's running on `mongodb://localhost:27017`
- **MongoDB Atlas**: Use your connection string

### Step 2: Setup Backend

```bash
# Navigate to backend directory
cd backend

# Create virtual environment (optional but recommended)
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file (copy from .env.example)
# Edit .env with your MongoDB URL and API keys

# Start the server
uvicorn app.main:app --reload --port 8000
```

**Backend will run on:** http://localhost:8000

### Step 3: Seed Database

Open a new terminal and run:
```bash
curl -X POST http://localhost:8000/seed
```

Or use Postman/Thunder Client:
- Method: POST
- URL: http://localhost:8000/seed

This will populate 6 sample restaurants with menu items.

### Step 4: Setup Frontend

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Create .env.local file (copy from .env.local.example)
# Edit .env.local with your API URL and Google Maps key

# Start the development server
npm run dev
```

**Frontend will run on:** http://localhost:3000

### Step 5: Access the Application

1. Open browser: http://localhost:3000
2. Register a new account or login
3. Browse restaurants, add items to cart, and place orders!

## 📝 Environment Variables Setup

### Backend `.env` file:
```env
MONGODB_URL=mongodb://localhost:27017/zomato_db
SECRET_KEY=your-secret-key-minimum-32-chars-change-in-production
GOOGLE_MAPS_API_KEY=your-google-maps-api-key
ACCESS_TOKEN_EXPIRE_MINUTES=1440
```

### Frontend `.env.local` file:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_GOOGLE_MAPS_KEY=your-google-maps-api-key
```

## 🔑 Getting Google Maps API Key

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable "Geocoding API"
4. Create credentials (API Key)
5. Copy the API key to both `.env` files

## ✅ Verify Everything Works

1. **Backend API**: Visit http://localhost:8000/docs (Swagger UI)
2. **Frontend**: Visit http://localhost:3000
3. **Test Flow**:
   - Register → Login → Browse → Add to Cart → Place Order → Track Order

## 🐛 Troubleshooting

- **Backend won't start**: Check MongoDB is running and `.env` file exists
- **Frontend can't connect**: Verify `NEXT_PUBLIC_API_URL` matches backend URL
- **Location not working**: Check Google Maps API key is set correctly
- **Database errors**: Run seed endpoint again to populate data

## 📚 API Documentation

Once backend is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
