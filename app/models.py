from pydantic import BaseModel, EmailStr

class ClientUser(BaseModel):
    email: EmailStr
    password: str
    full_name: str = ""

class OpsUser(BaseModel):
    email: EmailStr
    password: str
