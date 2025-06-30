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

# ---------------------------------- COMENTARIOS EXPLICATIVOS ----------------------------------

# Importa FastAPI para crear la aplicación web, HTTPException para manejar errores, y Depends para inyectar dependencias.
# Importa Session desde SQLAlchemy para manejar sesiones de base de datos.

# from db.conexion import Base, engine, SessionLocal:
#   - Base: Clase base usada para definir modelos con SQLAlchemy.
#   - engine: Motor de conexión a la base de datos.
#   - SessionLocal: Clase que crea sesiones para interactuar con la base de datos.

# from models.usuario import Usuario:
#   - Importa el modelo ORM que representa la tabla `usuarios`.

# from models.schemas import UsuarioCreate:
#   - Importa el esquema de validación de datos que se usa para crear nuevos usuarios (con Pydantic).

# from utils.seguridad import encriptar_contraseña:
#   - Importa la función que encripta la contraseña del usuario antes de guardarla en la base de datos.

# app = FastAPI():
#   - Inicializa la aplicación FastAPI.

# Base.metadata.create_all(bind=engine):
#   - Crea todas las tablas en la base de datos basadas en los modelos definidos con Base.
#   - Si ya existen, no las vuelve a crear.

# @app.get("/"):
#   - Define un endpoint en la raíz que responde a peticiones GET.
#   - Sirve para verificar si el servidor está corriendo correctamente.

# def get_db():
#   - Es una función que sirve como dependencia en los endpoints para obtener una sesión de base de datos.
#   - Usa `yield` para devolver la sesión y luego asegura que se cierre con `finally`.

# @app.post("/usuarios/"):
#   - Define un endpoint POST para crear un nuevo usuario.
#   - Recibe un objeto tipo UsuarioCreate (valores validados).
#   - Usa Depends(get_db) para acceder a la base de datos.

# usuario_existente = db.query(Usuario).filter(Usuario.correo == usuario.correo).first():
#   - Busca en la base de datos si ya existe un usuario con el mismo correo.

# if usuario_existente:
#   - Si encuentra un usuario con el correo dado, lanza un error HTTP 400 con un mensaje apropiado.

# usuario_nuevo = Usuario(...):
#   - Crea una instancia del modelo Usuario con los datos del formulario y la contraseña encriptada.

# db.add(usuario_nuevo), db.commit(), db.refresh(usuario_nuevo):
#   - add(): Agrega el usuario a la sesión.
#   - commit(): Guarda los cambios en la base de datos.
#   - refresh(): Refresca el objeto para obtener datos actualizados desde la base de datos (como el ID generado automáticamente).

# return {"mensaje": ..., "id": ...}:
#   - Retorna una respuesta JSON con un mensaje de éxito y el ID del nuevo usuario.

# -----------------------------------------------------------------------------------------------
