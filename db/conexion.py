from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Datos de conexión
USER = "root"
PASSWORD = "Corchea182"
HOST = "localhost"
PORT = "3306"
DATABASE = "facebook_clone"

# URL de conexión a MySQL
DATABASE_URL = f"mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"

# Crear el motor y la sesión
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para modelos
Base = declarative_base()
