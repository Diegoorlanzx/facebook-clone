from pydantic import BaseModel, EmailStr

class UsuarioCreate(BaseModel):
    nombre: str
    correo: EmailStr
    password: str

class UsuarioLogin(BaseModel):
    correo: EmailStr
    password: str
