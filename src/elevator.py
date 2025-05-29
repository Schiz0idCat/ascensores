import pygame
import time
from config.settings import BUILDING, TXT


# crear_ascensor(posicion_columna, piso_inicial, total_pisos)
# Crea un diccionario que representa un elevator.
#
# Parámetros:
#  - column (int): posición horizontal del elevator (respecto a las coordenadas de l edificio).
#  - currentFloor (int): piso inicial donde se encuentra el elevator (respecto a las coordenadas de l edificio).
#  - floors (int): número total de pisos del edificio.
#  - targets (list): targets a los que debe ir el elevator
def makeElevator(column, currentFloor, floors, targets, mutex):
    return {
        "column": BUILDING["COORD"][0] + column,               # columna del edificio donde se ubica
        "currentFloor": BUILDING["COORD"][1] + currentFloor,   # piso actual
        "state": "stop",                                       # "up", "down" o "stop"
        "floors": floors,                                      # cantidad de pisos
        "targets": targets,                                    # lista de los pisos a los que va
        "capacity": TXT["elevatorCapacity"],                   # capacidad máxima de personas
        "mutex": mutex 
    }


# dibujar_ascensor(screen, elevator, cellSize, color, colorDirection)
# Dibuja un elevator en la pantalla, centrado dentro de su celda correspondiente.
#
# Parámetros:
#  - screen (pygame.surface.Surface): superficie donde se dibujará el elevator.
#  - elevator (dict): diccionario con los datos del elevator (como el retornado por crear_ascensor).
#  - cellSize (int): tamaño de las celdas de la matriz.
#  - color (tuple): color de relleno del elevator (RGB).
#  - colorDirection (tuple): color de la línea que indica la dirección de movimiento.
def drawElevator(screen, elevator, cellSize, color, colorDirection):
    col = elevator["column"]
    piso = elevator["currentFloor"]
    state = elevator["state"]

    # Calcular posición centrada en la celda
    size = int(cellSize * 0.8)
    offset = (cellSize - size) // 2

    x = col * cellSize + offset
    y = screen.get_height() - (piso + 1) * cellSize + offset

    rect = pygame.Rect(x, y, size, size)
    pygame.draw.rect(screen, color, rect)

    # Dibujar arista según state
    if state == "up":
        pygame.draw.line(screen, colorDirection, (x, y), (x + size, y), 2)
    elif state == "down":
        pygame.draw.line(screen, colorDirection, (x, y + size), (x + size, y + size), 2)


# goto(elevator, destino, delay)
# Mueve un elevator hacia un piso de destino, modificando su state y posición gradualmente.
#
# Parámetros:
#  - elevator (dict): diccionario que representa el elevator que va a mover.
#  - delay (float): tiempo de espera entre movimientos, en segundos (por defecto 1s).
def goto(elevator, delay=1):
    while True: # Mantiene vivo el hilo
        time.sleep(delay)

        if len(elevator["targets"]) == 0:
            elevator["state"] = "stop"
        else:
            target = elevator["targets"][0]

            if elevator["currentFloor"] < target:
                elevator["targets"].sort()
                elevator["state"] = "up"
                elevator["currentFloor"] += 1
            elif elevator["currentFloor"] > target:
                elevator["targets"].sort(reverse=True)
                elevator["state"] = "down"
                elevator["currentFloor"] -= 1
            else:
                elevator["state"] = "stop"
                elevator["targets"].pop(0)

