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
        "currentFloor": currentFloor,
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
def drawPerson(screen, person, cellSize, peoplePerCell, color):
    if person["elevator"] != None:
        y = person["elevator"]["currentFloor"]
        x = person["elevator"]["column"]

        if (x, y) not in peoplePerCell:
            peoplePerCell[(x, y)] = []

        if person not in peoplePerCell[(x, y)]:
            peoplePerCell[(x, y)].append(person)
    else:
        # Dibujo normal, al lado del edificio
        x = BUILDING["COORD"][0] + BUILDING["COLS"]
        y = BUILDING["COORD"][1] + person["currentFloor"]
        maxPerCell = 5

        # Buscar celda válida para esta persona
        while True:
            if (x, y) not in peoplePerCell:
                peoplePerCell[(x, y)] = []

            if person in peoplePerCell[(x, y)]:
                break

            if len(peoplePerCell[(x, y)]) < maxPerCell:
                peoplePerCell[(x, y)].append(person)
                break

            x += 1

    screen_height = screen.get_height()
    x0 = x * cellSize
    y0 = screen_height - (y + 1) * cellSize

    peopleInCell = peoplePerCell[(x, y)]
    total = len(peopleInCell)
    index = peopleInCell.index(person)

    positions = {
        1: [(0.5, 0.5)],
        2: [(0.3, 0.3), (0.7, 0.7)],
        3: [(0.3, 0.3), (0.7, 0.3), (0.5, 0.7)],
        4: [(0.3, 0.3), (0.7, 0.3), (0.3, 0.7), (0.7, 0.7)],
        5: [(0.3, 0.3), (0.7, 0.3), (0.3, 0.7), (0.7, 0.7), (0.5, 0.5)],
    }

    relative_positions = positions[total]
    relX, relY = relative_positions[index]
    cx = int(x0 + relX * cellSize)
    cy = int(y0 + relY * cellSize)

    # Radio específico por cantidad de personas
    radiusPerPerson = {
        1: cellSize // 2.5,
        2: cellSize // 3.5,
        3: cellSize // 4.5,
        4: cellSize // 5,
        5: cellSize // 5.5,
    }

    radius = radiusPerPerson[total]

    pygame.draw.circle(screen, color, (cx, cy), radius)
    pygame.draw.circle(screen, (0, 0, 0), (cx, cy), radius, 2)

    # Renderizar el número del piso destino
    font_size = int(max(radius, 10))
    font = pygame.font.Font(None, font_size)
    text_surface = font.render(str(person["target"]), True, (0, 0, 0))
    text_rect = text_surface.get_rect(center=(cx, cy))
    screen.blit(text_surface, text_rect)

def removePersonFromCell(person, y, peoplePerCell):
    for (_, keyY), people in peoplePerCell.items():
        if keyY == y and person in people:
            people.remove(person)


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
