from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from .database import Base
""" Importa la clase base declarativa (Base) desde tu archivo database.py.	Es el punto de partida para definir modelos.
Esta clase proviene de: Base = declarative_base()"""

class User(Base):
	__tablename__ = "users"
	id = Column(String, primary_key=True, index=True)
	nickname = Column(String)

class Level(Base):
	__tablename__ = "levels"
	id = Column(Integer, primary_key=True, index=True)
	name = Column(String)
	time_limit = Column(Integer)
	words = relationship("Word", back_populates="level")

class Word(Base):
	__tablename__ = "words"
	id = Column(Integer, primary_key=True)
	word = Column(String)
	level_id = Column(Integer, ForeignKey("levels.id")) # (many-to-one)
	level = relationship("Level", back_populates="words")
		
class GameSession(Base):
	__tablename__ = "game_sessions"
	id = Column(Integer, primary_key=True, index=True)
	user_id = Column(String, ForeignKey("users.id")) # (1:N) un usuario puede tener múltiples sesiones de juego
	level_id = Column(Integer, ForeignKey("levels.id")) # (1:N)
	time_used = Column(Integer, default=0)
	solved = Column(Boolean, default=False)