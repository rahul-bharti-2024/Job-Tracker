# app/schemas/auth.py
from pydantic import BaseModel

class SignupRequest(BaseModel):
    email: str
    password: str

class AuthResponse(BaseModel):
    access_token: str
