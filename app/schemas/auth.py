from pydantic import BaseModel


class AdminLogin(BaseModel):
    username: str
    password: str


class AdminCreate(BaseModel):
    username: str
    password: str
    full_name: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    admin_name: str