from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from fastapi.requests import Request
from sqlalchemy.orm import Session

from db.conexion import Base, engine, SessionLocal
from models.usuario import Usuario
from models.schemas import UsuarioCreate, UsuarioLogin
from utils.seguridad import encriptar_contraseña, pwd_context
from utils.auth import crear_token, obtener_usuario_actual

# Mensaje de arranque
print("✅ ¡Servidor FastAPI está usando este archivo correctamente!")

# Crear la app
app = FastAPI()

# Configuración CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Crear las tablas en la BD
Base.metadata.create_all(bind=engine)

# Endpoint raíz
@app.get("/")
def read_root():
    return {"message": "Facebook Clone API is running"}

# Endpoint para solicitudes preflight (CORS)
@app.options("/{rest_of_path:path}", include_in_schema=False)
async def preflight_handler(request: Request, rest_of_path: str):
    return Response(status_code=200)

# Dependencia para obtener la sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Crear usuario
@app.post("/usuarios/")
def crear_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    usuario_existente = db.query(Usuario).filter(Usuario.correo == usuario.correo).first()
    if usuario_existente:
        raise HTTPException(status_code=400, detail="El correo ya está registrado")

    usuario_nuevo = Usuario(
        nombre=usuario.nombre,
        correo=usuario.correo,
        contraseña=encriptar_contraseña(usuario.password)
    )
    db.add(usuario_nuevo)
    db.commit()
    db.refresh(usuario_nuevo)
    return {"mensaje": "Usuario creado con éxito", "id": usuario_nuevo.id}

# Login
@app.post("/login/")
def login(usuario: UsuarioLogin, db: Session = Depends(get_db)):
    usuario_encontrado = db.query(Usuario).filter(Usuario.correo == usuario.correo).first()
    if not usuario_encontrado or not pwd_context.verify(usuario.password, usuario_encontrado.contraseña):
        raise HTTPException(status_code=400, detail="Correo o contraseña incorrectos")

    token = crear_token({"sub": usuario_encontrado.correo})
    return {"access_token": token, "token_type": "bearer"}

# Perfil privado (requiere token)
@app.get("/perfil/")
def perfil(usuario_actual: dict = Depends(obtener_usuario_actual)):
    return {"mensaje": "Este es tu perfil privado", "usuario": usuario_actual["sub"]}
