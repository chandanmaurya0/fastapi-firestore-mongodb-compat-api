import os
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

# Database configurations
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "fastapi_mongodb")

# Global database connection
client = None
db = None

async def init_db():
    """Initialize database connection"""
    global client, db
    try:
        client = AsyncIOMotorClient(MONGODB_URL)
        db = client[DB_NAME]
        # Test the connection
        await db.command('ping')
        print("Successfully connected to MongoDB!")
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        raise

def get_database():
    """Get database instance"""
    if db is None:
        raise RuntimeError("Database not initialized. Call init_db() first.")
    return db

async def close_db():
    """Close database connection"""
    if client:
        client.close()
