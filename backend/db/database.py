from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Cambia estos valores por los tuyos
USER = "root"
PASSWORD = "Corchea182"
HOST = "localhost"
PORT = "3306"
DATABASE = "facebook_clone"

# URL de conexión: dialect+driver://usuario:contraseña@host:puerto/basededatos
DATABASE_URL = f"mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"

# Crea el engine para conectarse a la base de datos
engine = create_engine(DATABASE_URL, echo=True)

# Session: es la clase para hacer consultas
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base: clase base para los modelos (tablas)
Base = declarative_base()
