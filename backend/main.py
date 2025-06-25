from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

# Importaciones internas
from db.conexion import Base, engine, SessionLocal
from models.usuario import Usuario
from models.schemas import UsuarioCreate
from utils.seguridad import encriptar_contraseña

# Inicializar FastAPI
app = FastAPI()

# Crear las tablas en la base de datos si no existen
Base.metadata.create_all(bind=engine)

# Endpoint raíz
@app.get("/")
def read_root():
    return {"message": "Facebook Clone API is running"}

# Dependencia para obtener la sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint para crear un nuevo usuario
@app.post("/usuarios/")
def crear_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    usuario_existente = db.query(Usuario).filter(Usuario.correo == usuario.correo).first()
    if usuario_existente:
        raise HTTPException(status_code=400, detail="El correo ya está registrado")

    usuario_nuevo = Usuario(
        nombre=usuario.nombre,
        correo=usuario.correo,
        contraseña=encriptar_contraseña(usuario.contraseña)
    )
    db.add(usuario_nuevo)
    db.commit()
    db.refresh(usuario_nuevo)
    return {"mensaje": "Usuario creado con éxito", "id": usuario_nuevo.id}
