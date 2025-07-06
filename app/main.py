from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database.db import init_db
from app.routes import user_route

app = FastAPI(
    title="FastAPI MongoDB App",
    description="A FastAPI application with MongoDB",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database connection
@app.on_event("startup")
async def startup_db_client():
    await init_db()

# Include routers
app.include_router(user_route.router)

# Health check endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI with MongoDB!"}



