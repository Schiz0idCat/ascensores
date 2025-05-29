import pygame
import random
import time
from config.settings import BUILDING


# makePerson(target, currentFloor, color)
# Crea un diccionario que representa a una persona con target, currentFloor actual y color.
#
# Parámetros:
#  - target (int): currentFloor al que la persona quiere ir.
#  - currentFloor (int): currentFloor en el que se encuentra actualmente la persona.
#  - color (tuple): color RGB para dibujar a la persona.
#  - elevator (dict): ascensor al que se sube (si no está dentro de ninguno, es None)
def makePerson(target, currentFloor, color, elevator):
    return {
        "target": target,
        "currentFloor": BUILDING["COORD"][1] + currentFloor,
        "color": color,
        "elevator": elevator
    }


# drawPerson(screen, persona, cellSize, personasPorCelda, color)
# Dibuja una persona en la pantalla en una celda adyacente al edificio
# Si no hay espacio para la persona en la celda en la que la vaya a dibujar,
# Entonces se intenta dibujar en la celda de la derecha (así hasta encontrar una celda)
#
# Parámetros:
#  - screen (pygame.Surface): superficie donde se dibujará la persona.
#  - person (dict): diccionario con los datos de la persona.
#  - cellSize (int): tamaño de la celda para posicionar la persona.
#  - peoplePerCell (dict): diccionario que mapea celdas a listas de personas que ocupan esa celda.
#  - color (tuple): color RGB para dibujar la persona.
def drawPerson(screen, person, cellSize, peoplePerCell, color, maxPeople=5):
    if person["elevator"] != None:
        y = person["elevator"]["currentFloor"]
        x = person["elevator"]["column"]

        # Validar rango
        if 0 <= x < len(peoplePerCell) and 0 <= y < len(peoplePerCell[0]):
            if person not in peoplePerCell[x][y]:
                if len(peoplePerCell[x][y]) < maxPeople:
                    peoplePerCell[x][y].append(person)

    else:
        x = BUILDING["COORD"][0] + BUILDING["COLS"]
        y = BUILDING["COORD"][1] + person["currentFloor"]

        # Buscar celda válida dentro del rango
        while True:
            if x >= len(peoplePerCell):
                break  # Fuera de rango horizontal, no agregamos
            
            if y >= len(peoplePerCell[0]):
                break  # Fuera de rango vertical, no agregamos

            if person in peoplePerCell[x][y]:
                break

            if len(peoplePerCell[x][y]) < maxPeople:
                peoplePerCell[x][y].append(person)
                break

            x += 1

    screen_height = screen.get_height()
    x0 = x * cellSize
    y0 = screen_height - (y + 1) * cellSize

    if 0 <= x < len(peoplePerCell) and 0 <= y < len(peoplePerCell[0]):
        peopleInCell = peoplePerCell[x][y]
    else:
        peopleInCell = []

    total = len(peopleInCell)
    if person in peopleInCell:
        index = peopleInCell.index(person)
    else:
        index = 0

    positions = {
        1: [(0.5, 0.5)],
        2: [(0.3, 0.3), (0.7, 0.7)],
        3: [(0.3, 0.3), (0.7, 0.3), (0.5, 0.7)],
        4: [(0.3, 0.3), (0.7, 0.3), (0.3, 0.7), (0.7, 0.7)],
        5: [(0.3, 0.3), (0.7, 0.3), (0.3, 0.7), (0.7, 0.7), (0.5, 0.5)],
    }

    if total == 0:
        return  # No dibujar si no hay personas

    relative_positions = positions[total]
    rel_x, rel_y = relative_positions[index]
    cx = int(x0 + rel_x * cellSize)
    cy = int(y0 + rel_y * cellSize)

    radio_por_personas = {
        1: cellSize // 2.5,
        2: cellSize // 3.5,
        3: cellSize // 4.5,
        4: cellSize // 5,
        5: cellSize // 5.5,
    }

    radius = radio_por_personas[total]

    pygame.draw.circle(screen, color, (cx, cy), radius)
    pygame.draw.circle(screen, (0, 0, 0), (cx, cy), radius, 2)

    font_size = int(max(radius, 10))
    font = pygame.font.Font(None, font_size)
    text_surface = font.render(str(person["target"]), True, (0, 0, 0))
    text_rect = text_surface.get_rect(center=(cx, cy))
    screen.blit(text_surface, text_rect)


def removePersonFromCell(person, y, peoplePerCell):
    if 0 <= y < len(peoplePerCell[0]):
        for x in range(len(peoplePerCell)):
            if person in peoplePerCell[x][y]:
                peoplePerCell[x][y].remove(person)


def goto(elevators, person, peoplePerCell, delay=1):
    time.sleep(delay)
    elevator = random.choice(elevators)

    if len(elevator["targets"]) >= elevator["capacity"]:
        return

    # bloquear array para todos los demás
    elevator["targets"].append(person["target"])
    person["elevator"] = elevator
    removePersonFromCell(person, person["currentFloor"], peoplePerCell)
    # desbloquear array para todos los demás
    
    # subirAlElevador()

    while person["currentFloor"] != person["target"]:
        person["currentFloor"] = elevator["currentFloor"]
        time.sleep(delay)

    # bajarDelElevador()

    person["elevator"] = None

