from fastapi import APIRouter, Depends, HTTPException, status
from app.models.users import UserRegister, UserLogin, UserData, UserSave
from app.database import db
from datetime import datetime
from app.utils.security import hash_password, verify_password, create_access_token


router = APIRouter(prefix="/auth", tags=["authentication"])
@router.post("/register")
async def register_user(user_data: UserRegister):
  existing_user=await db.users.find_one({"email": user_data.email})
  if existing_user:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cet email est déjà utilisé.")
  hashed = hash_password(user_data.password)
  new_user = {
    "username":user_data.username,
    "email": user_data.email,
    "hashed_password": hashed,
    "created_at": datetime.utcnow(),
    
  }
  result = await db.users.insert_one(new_user)
  return{
    "message":"Utilisareur enregistré avec succès",
    "user_id": str(result.inserted_id)
  }

@router.post("/login")
async def login_user(login_data: UserLogin):
  user=await db.users.find_one({"email": login_data.email})
  if not user or not verify_password(login_data.password, user["hashed_password"]):
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email ou mot de passe incorrect.")
  access_token=create_access_token(data={"sub":user["email"]})
  return{
    "access_token":access_token,
    "token_type":"bearer",
    "username": user["username"],
    "userEmail":user["email"]
  
  }

  