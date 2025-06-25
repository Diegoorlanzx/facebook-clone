from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def encriptar_contraseña(contraseña: str) -> str:
    return pwd_context.hash(contraseña)
