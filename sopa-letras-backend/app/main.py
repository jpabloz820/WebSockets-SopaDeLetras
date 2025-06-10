from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import game, users
from app.websocket import router as ws_router

app = FastAPI()

# 🎯 Habilita CORS para permitir solicitudes desde el frontend (React)
origins = [
    "http://localhost:3000",  # Asegúrate de que coincida con el puerto de tu frontend
    "http://127.0.0.1:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # ✅ Permitir estos orígenes
    allow_credentials=True,
    allow_methods=["*"],              # ✅ Permitir todos los métodos (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],              # ✅ Permitir todos los headers
)

# 📦 Incluye tus routers
app.include_router(game.router)
app.include_router(users.router)
app.include_router(ws_router)