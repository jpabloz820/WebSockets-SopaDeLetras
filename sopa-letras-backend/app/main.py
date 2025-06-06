from fastapi import FastAPI
from app.routers import game, users
from app.websocket import router as ws_router

app = FastAPI() # 🚀 Crea una instancia de la aplicación FastAPI.
app.include_router(game.router)
app.include_router(users.router)
app.include_router(ws_router) # rutas WebSocket para comunicación en tiempo real.