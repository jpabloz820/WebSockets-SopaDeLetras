from sqlalchemy import create_engine # Crea la conexión a la base de datos
from sqlalchemy.ext.declarative import declarative_base # Crea una clase base desde la cual derivar tus modelos.
from sqlalchemy.orm import sessionmaker # Permite crear sesiones para interactuar con la base de datos.

DATABASE_URL = "postgresql://postgres:1234@localhost:5432/sopaletras"

engine = create_engine(DATABASE_URL) #Esto crea el motor de conexión con PostgreSQL usando la URL.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) # Esto prepara una fábrica de sesiones, que se usará para leer/escribir datos en la base.

Base = declarative_base() # Esto es la clase base desde la cual heredan todos tus modelos (User, Game, etc.).