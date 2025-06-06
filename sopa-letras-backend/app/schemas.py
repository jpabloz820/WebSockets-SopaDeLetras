from pydantic import BaseModel # BaseModel de Pydantic, base para crear modelos de datos.
from typing import List, Optional

class UserBase(BaseModel):
	nickname: str

class UserCreate(UserBase):
	pass

class User(UserBase):
	id: str # (strings)

	class Config:
		orm_mode = True # Habilita orm_mode para trabajar con ORM (Mapeo Objeto-Relacional)

class LevelBase(BaseModel):
	name: str
	time_limit: int

class LevelCreate(LevelBase):
	pass

class Level(LevelBase):
	id: int

	class Config:
		orm_mode = True

class WordBase(BaseModel):
	word: str
	level_id: int

class WordCreate(WordBase):
	pass

class Word(WordBase):
	id: int

	class Config:
		orm_mode = True

class GameSessionBase(BaseModel):
	user_id: str
	level_id: int
	time_used: Optional[int] = 0  # Segundos
	solved: Optional[bool] = False

class GameSessionCreate(GameSessionBase):
	pass

class GameSession(GameSessionBase):
	id: int

	class Config:
		orm_mode = True

# Para iniciar juego y enviar tablero dinámico y tiempo

class StartGameResponse(BaseModel):
	board: List[List[str]]
	time_limit: int
	words: List[str]
