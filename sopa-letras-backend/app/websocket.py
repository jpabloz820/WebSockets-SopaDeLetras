from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import asyncio
import json
import time

router = APIRouter()
games = {}  # Guardar estado del juego por conexión


@router.websocket("/ws/game")
async def game_ws(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_text("Conectado")

    try:
        start_time = time.time()

        while True:
            data = await websocket.receive_text()
            msg = json.loads(data)

            if msg["command"] == "start":
                # Guardar tablero y palabras en el estado
                board = msg["board"]
                words = msg["words"]
                games[websocket] = {
                    "board": board,
                    "words": words,
                    "start_time": time.time()
                }
                await websocket.send_text("Juego iniciado")

            elif msg["command"] == "solve":
                game = games.get(websocket)
                if not game:
                    await websocket.send_text(json.dumps({"command": "error", "message": "Juego no iniciado"}))
                    continue

                board = game["board"]
                words = game["words"]

                solved_words = []

                for word in words:
                    path = find_word_in_board(board, word)
                    if path:
                        solved_words.append({"word": word, "path": path})

                await websocket.send_text(json.dumps({
                    "command": "solve",
                    "words": solved_words
                }))

            elif msg["command"] == "time":
                elapsed = int(time.time() - start_time)
                await websocket.send_text(json.dumps({"command": "time", "elapsed": elapsed}))

            else:
                await websocket.send_text(f"Comando desconocido: {msg['command']}")

    except WebSocketDisconnect:
        print("Cliente desconectado")
        if websocket in games:
            del games[websocket]


def find_word_in_board(board, word):
    word = word.upper()
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0

    # Horizontal y vertical
    for r in range(rows):
        for c in range(cols):
            if check_word(board, word, r, c, 0, 1):  # Horizontal derecha
                return [(r, c + i) for i in range(len(word))]
            if check_word(board, word, r, c, 1, 0):  # Vertical abajo
                return [(r + i, c) for i in range(len(word))]
            if check_word(board, word, r, c, 0, -1):  # Horizontal izquierda
                return [(r, c - i) for i in range(len(word))]
            if check_word(board, word, r, c, -1, 0):  # Vertical arriba
                return [(r - i, c) for i in range(len(word))]

    return None


def check_word(board, word, r, c, dr, dc):
    for i in range(len(word)):
        nr, nc = r + dr * i, c + dc * i
        if not (0 <= nr < len(board)) or not (0 <= nc < len(board[0])):
            return False
        if board[nr][nc].upper() != word[i]:
            return False
    return True
