from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status

# Configuración del JWT
SECRET_KEY = "clave_secreta_super_segura"  # cámbiala por una segura en producción
ALGORITHM = "HS256"
EXPIRATION_MINUTES = 30

# Función para crear el token JWT
def crear_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=EXPIRATION_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Función para verificar y decodificar el token
def verificar_token(token: str) -> dict | None:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Dependencia para obtener el usuario autenticado
def obtener_usuario_actual(token: str = Depends(oauth2_scheme)):
    credenciales_invalidas = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido o expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = verificar_token(token)
    if payload is None:
        raise credenciales_invalidas
    return payload