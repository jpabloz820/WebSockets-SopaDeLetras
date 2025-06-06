import threading # para realizar tareas en paralelo.
import random
import string
# Importa el módulo string, que tiene constantes útiles como string.ascii_uppercase (letras mayúsculas de A-Z).

DIRECTIONS = [(0,1), (1,0)]  # derecha y abajo

def can_place_word(board, word, row, col, direction):
	dr, dc = direction # dr, dc: desplazamientos por dirección.
	rows = len(board) # rows: número de filas en el tablero.
	cols = len(board[0]) # cols: número de columnas en el tablero.

	for i in range(len(word)): # Recorre cada letra de la palabra y calcula su posición final.
		r = row + dr*i
		c = col + dc*i
		if r >= rows or c >= cols: # Verifica que no se salga del tablero.
			return False
		if board[r][c] != word[i] and board[r][c] != ' ':
			return False
	return True

"""if board[r][c] != word[i] and board[r][c] != ' ':
	Esta validación permite:
	Colocar letras en celdas vacías (' ').
	Colocar letras encima de letras iguales (por ejemplo, dos palabras cruzando por la misma letra).
	Evita sobrescribir letras diferentes, que dañaría otras palabras del tablero."""
		
def place_word(board, word):
	rows = len(board) # número de filas del tablero.
	cols = len(board[0]) # número de columnas del tablero.

	placed = False # indica si la palabra se ha colocado correctamente (true).
	attempts = 0 # contador de intentos para colocar la palabra.
	while not placed and attempts < 100:
		direction = random.choice(DIRECTIONS) # Selecciona una dirección aleatoria (horizontal o vertical).
		max_row = rows - (len(word) if direction[0] != 0 else 1) #Calcula el límite máximo de fila desde donde puede comenzar la palabra sin salirse.
		max_col = cols - (len(word) if direction[1] != 0 else 1) # Calcula el límite máximo de columna desde donde puede comenzar la palabra sin salirse.
		row = random.randint(0, max_row) # Selecciona una fila aleatoria dentro del rango permitido.
		col = random.randint(0, max_col) # Selecciona una columna aleatoria dentro del rango permitido.

		if can_place_word(board, word, row, col, direction): # Verifica si se puede colocar la palabra en la posición y dirección seleccionadas.
			dr, dc = direction # Descompone la dirección en desplazamientos de fila (dr) y columna (dc).
			for i, ch in enumerate(word): # Recorre cada letra de la palabra junto con su índice.
				board[row + dr*i][col + dc*i] = ch # Coloca la letra en la posición correspondiente del tablero.
			placed = True
		attempts += 1
	if not placed:
		print(f"No se pudo colocar la palabra: {word}")

def generate_board(rows, cols, words): # Se define una función que genera un tablero de sopa de letras.
	board = [[random.choice(string.ascii_uppercase) for _ in range(cols)] for _ in range(rows)]
	""" Crea una matriz 2D (lista de listas) llamada board, de tamaño rows x cols,
		llena de letras mayúsculas aleatorias."""

	threads = [] # 🧵 Crea una lista vacía para almacenar los threads que se van a ejecutar.
	for word in words: # 🔁 Recorre cada palabra que se quiere insertar en el tablero.
		t = threading.Thread(target=place_word, args=(board, word)) # 🔧 Crea un nuevo hilo (Thread) que ejecutará la función place_word con la palabra como argumento.
		t.start() # ▶️ Inicia el hilo: esto hace que insert_word(word) se ejecute en paralelo con el resto del programa.
		threads.append(t) # ➕ Guarda el hilo en la lista threads para poder esperar a que termine más adelante.

	for t in threads:
		t.join()
		""" 🔚 Espera a que todos los hilos terminen su ejecución. 
			Esto asegura que todas las palabras se hayan insertado en el tablero antes de continuar."""
	return board
