from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import uuid # para generar identificadores únicos.
from app import models, schemas
from app.database import SessionLocal

router = APIRouter(prefix="/users", tags=["users"]) # El tag es solo para documentación automática (Swagger).

def get_db():
	db = SessionLocal()
	try:
		yield db # Usa yield para hacerla generadora, así FastAPI puede abrir y cerrar la sesión automáticamente.
	finally:
		db.close()

@router.post("/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
	# Generamos un UUID para el usuario
	user_id = str(uuid.uuid4())
	db_user = models.User(id=user_id, nickname=user.nickname)
	db.add(db_user)
	db.commit()
	db.refresh(db_user)
	return db_user

@router.get("/{user_id}", response_model=schemas.User)
def get_user(user_id: str, db: Session = Depends(get_db)):
	db_user = db.query(models.User).filter(models.User.id == user_id).first()
	if not db_user:
		raise HTTPException(status_code=404, detail="Usuario no encontrado")
	return db_user
