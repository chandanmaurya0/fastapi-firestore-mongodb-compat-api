from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends, status, Query
from bson import ObjectId
from datetime import datetime, timezone

from app.database.db import get_database
from app.models.user import UserBase, UserCreate, UserInDB, UserUpdate
from app.utils.security import get_password_hash

router = APIRouter(prefix="/users", tags=["users"])

# Helper function to convert MongoDB document to UserInDB
def user_helper(user) -> dict:
    return {
        "id": str(user["_id"]),
        "user_id": user["user_id"],
        "full_name": user["full_name"],
        "email": user["email"],
        "city": user["city"],
        "is_active": user["is_active"],
        "created_at": user["created_at"],
        "updated_at": user["updated_at"]
    }

@router.post("/", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
    """
    Create a new user.
    """
    # Check if user_id already exists
    if await get_database().users.find_one({"user_id": user.user_id}):
        raise HTTPException(
            status_code=400,
            detail="User with this user_id already exists"
        )
    
    # Check if email already exists
    if await get_database().users.find_one({"email": user.email}):
        raise HTTPException(
            status_code=400,
            detail="User with this email already exists"
        )
    
    # Hash the password
    hashed_password = get_password_hash(user.password)
    
    # Create user data
    user_data = user.dict(exclude={"password"})
    user_data["hashed_password"] = hashed_password
    user_data["created_at"] = datetime.now(timezone.utc)
    user_data["updated_at"] = datetime.now(timezone.utc)
    
    # Insert user into database
    result = await get_database().users.insert_one(user_data)
    
    # Return the created user
    new_user = await get_database().users.find_one({"_id": result.inserted_id})
    return {"message": "User created successfully", "user": user_helper(new_user)}

@router.get("/", response_model=List[dict])
async def get_users(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, le=100, description="Number of records to return"),
    is_active: Optional[bool] = None
):
    """
    Get all users with pagination and optional filtering by active status.
    """
    query = {}
    if is_active is not None:
        query["is_active"] = is_active
    
    users = []
    async for user in get_database().users.find(query).skip(skip).limit(limit):
        users.append(user_helper(user))
    
    return users

@router.get("/{user_id}", response_model=dict)
async def get_user(user_id: str):
    """
    Get a specific user by user_id.
    """
    user = await get_database().users.find_one({"user_id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user_helper(user)

@router.put("/{user_id}", response_model=dict)
async def update_user(user_id: str, user_update: UserUpdate):
    """
    Update a user's information.
    """
    # Check if user exists
    user = await get_database().users.find_one({"user_id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Prepare update data
    update_data = user_update.dict(exclude_unset=True)
    
    # If password is being updated, hash the new password
    if "password" in update_data:
        update_data["hashed_password"] = get_password_hash(update_data.pop("password"))
    
    # Add updated_at timestamp
    update_data["updated_at"] = datetime.now(timezone.utc)
    
    # Update user in database
    result = await get_database().users.update_one(
        {"user_id": user_id},
        {"$set": update_data}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=400, detail="No changes were made")
    
    # Return the updated user
    updated_user = await get_database().users.find_one({"user_id": user_id})
    return {"message": "User updated successfully", "user": user_helper(updated_user)}

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: str):
    """
    Delete a user.
    """
    # Check if user exists
    user = await get_database().users.find_one({"user_id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Soft delete by setting is_active to False
    await get_database().users.update_one(
        {"user_id": user_id},
        {"$set": {"is_active": False, "updated_at": datetime.now(timezone.utc)}}
    )
    
    return {"message": "User deactivated successfully"}

# Include this router in your main FastAPI app
# from fastapi import FastAPI
# from .routes import user_route
# app = FastAPI()
# app.include_router(user_route.router)