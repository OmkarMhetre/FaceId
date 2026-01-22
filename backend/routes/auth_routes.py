from fastapi import APIRouter
from pydantic import BaseModel

from backend.auth.auth_controller  import authenticate_admin
router = APIRouter()

class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/login")
def login(data: LoginRequest):
    return authenticate_admin(data.username, data.password)

