import threading
import random
import string

# Solo direcciones: derecha y abajo
DIRECTIONS = [(0, 1), (1, 0)]

# Lock global para sincronizar acceso al tablero
lock = threading.Lock()

def can_place_word(board, word, row, col, direction):
    dr, dc = direction
    rows = len(board)
    cols = len(board[0])

    for i in range(len(word)):
        r = row + dr * i
        c = col + dc * i
        if r >= rows or c >= cols:
            return False
        if board[r][c] != word[i] and board[r][c] != ' ':
            return False
    return True

def place_word(board, word, lock):
    rows = len(board)
    cols = len(board[0])
    placed = False
    attempts = 0

    while not placed and attempts < 100:
        direction = random.choice(DIRECTIONS)
        max_row = rows - (len(word) if direction[0] != 0 else 1)
        max_col = cols - (len(word) if direction[1] != 0 else 1)
        row = random.randint(0, max_row)
        col = random.randint(0, max_col)

        with lock:
            if can_place_word(board, word, row, col, direction):
                dr, dc = direction
                for i, ch in enumerate(word):
                    board[row + dr * i][col + dc * i] = ch
                placed = True
        attempts += 1

    if not placed:
        print(f"No se pudo colocar la palabra: {word}")

def generate_board(rows, cols, words):
    # Inicializa el tablero con espacios en blanco
    board = [[' ' for _ in range(cols)] for _ in range(rows)]

    threads = []
    for word in words:
        t = threading.Thread(target=place_word, args=(board, word, lock))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    # Rellenar espacios vacíos con letras aleatorias
    for r in range(rows):
        for c in range(cols):
            if board[r][c] == ' ':
                board[r][c] = random.choice(string.ascii_uppercase)

    return board

def print_board(board):
    for row in board:
        print(' '.join(row))

# === USO ===
words = ["GATO", "PERRO", "RATON", "AVE"]
board = generate_board(10, 10, words)
print_board(board)
