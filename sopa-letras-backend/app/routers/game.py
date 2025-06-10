from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, game_logic
from app.database import SessionLocal
import uuid

router = APIRouter(prefix="/game", tags=["game"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/levels", response_model=list[schemas.Level]) # Devuelve una lista de niveles (con su estructura definida en schemas.Level).
def get_levels(db: Session = Depends(get_db)):
    levels = db.query(models.Level).all()
    return levels

@router.post("/start", response_model=schemas.StartGameResponse) # Devuelve la información para iniciar un juego (tablero, palabras y tiempo).
def start_game(user_id: int, level_id: int, db: Session = Depends(get_db)):
    level = db.query(models.Level).filter(models.Level.id == level_id).first()
    if not level:
        raise HTTPException(status_code=404, detail="Nivel no encontrado")

    words = db.query(models.Word).filter(models.Word.level_id == level_id).all()
    words_list = [w.word.upper() for w in words] # Convierte cada palabra a mayúsculas.

    # Crear tablero dinámico con game_logic (usamos función existente)
    rows = cols = max(10, len(max(words_list, key=len)) + 2)  # Tamaño base ejemplo (10x10 o más grande si hay palabras largas) Se basa en la palabra más larga + margen (2)
    board = game_logic.generate_board(rows, cols, words_list)

    # Crear GameSession para este usuario y nivel
    session_id = str(uuid.uuid4())
    game_session = models.GameSession(user_id=user_id, level_id=level_id)
    db.add(game_session)
    db.commit()

    return schemas.StartGameResponse(
        board=board,
        time_limit=level.time_limit,
        words=words_list
    )

@router.get("/resolve/{level_id}", response_model=dict)
def resolve(level_id: int, db: Session = Depends(get_db)):
    # Retorna las posiciones de las palabras (implementa si quieres)
    # Por simplicidad, retornamos las palabras como están (mejor implementarlo con posiciones)
    words = db.query(models.Word).filter(models.Word.level_id == level_id).all()
    return {"words": [w.word.upper() for w in words]}