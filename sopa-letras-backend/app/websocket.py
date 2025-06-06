from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import asyncio
import json
import time

router = APIRouter()
""" Este objeto router servirá para definir rutas o endpoints (en este caso, un WebSocket)
	que luego pueden ser añadidos a la aplicación principal FastAPI."""

games = {}  # Guardar estado por conexión

""" Aquí se usa un decorador para definir que la función que viene a continuación será un manejador
	para conexiones WebSocket en la ruta /ws/game.
	Esto significa que cuando un cliente abra un WebSocket apuntando a esta URL, esta función responderá."""
@router.websocket("/ws/game")
async def game_ws(websocket: WebSocket):
	await websocket.accept()
	await websocket.send_text("Conectado")
	try:
		start_time = time.time() # Guarda el tiempo actual en segundos
		while True:
			data = await websocket.receive_text()   # Espera asíncronamente a que el cliente envíe un mensaje de texto a través del WebSocket.
													# El mensaje recibido se guarda en la variable data.
			msg = json.loads(data) # Convierte el mensaje JSON recibido en un diccionario de Python.

			# Ejemplo simple: recibe { "command": "echo", "message": "hola" }
			if msg["command"] == "echo":
				await websocket.send_text(f"Echo: {msg['message']}")
			elif msg["command"] == "solve":
				# Aquí mandarías las posiciones de las palabras
				# Por ahora enviamos mensaje de ejemplo
				await websocket.send_text(json.dumps({"command": "solve", "positions": "Aquí irían posiciones"}))
			elif msg["command"] == "time":
				elapsed = int(time.time() - start_time)
				await websocket.send_text(json.dumps({"command": "time", "elapsed": elapsed}))
			else:
				await websocket.send_text(f"Comando desconocido: {msg['command']}")

	except WebSocketDisconnect:
		print("Cliente desconectado")