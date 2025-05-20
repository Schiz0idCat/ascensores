import pygame
import time
from config.settings import BUILDING, TXT


# crear_ascensor(posicion_columna, piso_inicial, total_pisos)
# Crea un diccionario que representa un ascensor.
#
# Parámetros:
#  - columna (int): posición horizontal del ascensor (respecto a las coordenadas de l edificio).
#  - pisoActual (int): piso inicial donde se encuentra el ascensor (respecto a las coordenadas de l edificio).
#  - maxPisos (int): número total de pisos del edificio.
def crear_ascensor(columna: int, pisoActual: int, maxPisos: int):
    return {
        "columna": BUILDING["COORD"][0] + columna,         # columna del edificio donde se ubica
        "pisoActual": BUILDING["COORD"][1] + pisoActual,   # piso actual
        "estado": "detenido",                              # "subiendo", "bajando" o "detenido"
        "maxPisos": maxPisos,                              # cantidad de pisos
        "capacidad": TXT["maxPersonasAscensor"]            # capacidad máxima de personas
    }


# dibujar_ascensor(screen, ascensor, cellSize, color, colorDireccion)
# Dibuja un ascensor en la pantalla, centrado dentro de su celda correspondiente.
#
# Parámetros:
#  - screen (pygame.surface.Surface): superficie donde se dibujará el ascensor.
#  - ascensor (dict): diccionario con los datos del ascensor (como el retornado por crear_ascensor).
#  - cellSize (int): tamaño de las celdas de la matriz.
#  - color (tuple): color de relleno del ascensor (RGB).
#  - colorDireccion (tuple): color de la línea que indica la dirección de movimiento.
def dibujar_ascensor(screen, ascensor, cellSize, color, colorDireccion):
    col = ascensor["columna"]
    piso = ascensor["pisoActual"]
    estado = ascensor["estado"]

    # Calcular posición centrada en la celda
    size = int(cellSize * 0.8)
    offset = (cellSize - size) // 2

    x = col * cellSize + offset
    y = screen.get_height() - (piso + 1) * cellSize + offset

    rect = pygame.Rect(x, y, size, size)
    pygame.draw.rect(screen, color, rect)

    # Dibujar arista según estado
    if estado == "subiendo":
        pygame.draw.line(screen, colorDireccion, (x, y), (x + size, y), 2)
    elif estado == "bajando":
        pygame.draw.line(screen, colorDireccion, (x, y + size), (x + size, y + size), 2)

# goto(ascensor, destino, delay)
# Mueve un ascensor hacia un piso de destino, modificando su estado y posición gradualmente.
#
# Parámetros:
#  - ascensor (dict): diccionario que representa el ascensor.
#  - destino (int): piso al cual debe llegar el ascensor.
#  - delay (float): tiempo de espera entre movimientos, en segundos (por defecto 1s).
def goto(ascensor: dict, destino: int, delay: float = 1):
    while ascensor["pisoActual"] != destino:
        if ascensor["pisoActual"] < destino:
            ascensor["estado"] = "subiendo"
            ascensor["pisoActual"] += 1
        elif ascensor["pisoActual"] > destino:
            ascensor["estado"] = "bajando"
            ascensor["pisoActual"] -= 1

        time.sleep(delay)

    ascensor["estado"] = "detenido"
