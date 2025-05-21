import pygame
import random
import time
from config.settings import BUILDING


# makePerson(destino, piso, color)
# Crea un diccionario que representa a una persona con destino, piso actual y color.
#
# Parámetros:
#  - destino (int): piso al que la persona quiere ir.
#  - piso (int): piso en el que se encuentra actualmente la persona.
#  - color (tuple): color RGB para dibujar a la persona.
def makePerson(destino, piso, color, ascensor):
    return {
        "destino": destino,
        "piso": piso,
        "color": color,
        "elevator": ascensor
    }


# drawPerson(screen, persona, cellSize, personasPorCelda, color)
# Dibuja una persona en la pantalla en una celda adyacente al edificio
# Si no hay espacio para la persona en la celda en la que la vaya a dibujar,
# Entonces se intenta dibujar en la celda de la derecha (así hasta encontrar una celda)
#
# Parámetros:
#  - screen (pygame.Surface): superficie donde se dibujará la persona.
#  - persona (dict): diccionario con los datos de la persona.
#  - cellSize (int): tamaño de la celda para posicionar la persona.
#  - personasPorCelda (dict): diccionario que mapea celdas a listas de personas que ocupan esa celda.
#  - color (tuple): color RGB para dibujar la persona.
def drawPerson(screen, persona, cellSize, personasPorCelda, color):
    if persona["elevator"] != None:
        y = persona["elevator"]["pisoActual"]
        x = persona["elevator"]["columna"]

        if (x, y) not in personasPorCelda:
            personasPorCelda[(x, y)] = []

        if persona not in personasPorCelda[(x, y)]:
            personasPorCelda[(x, y)].append(persona)
    else:
        # Dibujo normal, al lado del edificio
        x = BUILDING["COORD"][0] + BUILDING["COLUMNAS"]
        y = BUILDING["COORD"][1] + persona["piso"]
        maxPorCelda = 1

        # Buscar celda válida para esta persona
        while True:
            if (x, y) not in personasPorCelda:
                personasPorCelda[(x, y)] = []

            if persona in personasPorCelda[(x, y)]:
                break

            if len(personasPorCelda[(x, y)]) < maxPorCelda:
                personasPorCelda[(x, y)].append(persona)
                break

            x += 1

    screen_height = screen.get_height()
    x0 = x * cellSize
    y0 = screen_height - (y + 1) * cellSize

    margin = 4
    max_radius = (cellSize - 2 * margin) // 2

    personasEnCelda = personasPorCelda[(x, y)]
    total = len(personasEnCelda)
    index = personasEnCelda.index(persona)

    # Calcular el radio para que no queden enormes
    if total > 1:
        radius = max_radius // total
        if radius < 2:
            radius = 2  # mínimo radio visible
    else:
        radius = max_radius

    spacing = cellSize // total
    cx = x0 + spacing * index + spacing // 2
    cy = y0 + cellSize // 2

    pygame.draw.circle(screen, color, (cx, cy), radius)
    pygame.draw.circle(screen, (0, 0, 0), (cx, cy), radius, 2)


def removePersonFromCell(person, y, peoplePerCell):
    for (_, clave_y), people in peoplePerCell.items():
        if clave_y == y and person in people:
            people.remove(person)


def goto(elevators, person, peoplePerCell, delay=1):
    time.sleep(delay)
    elevator = random.choice(elevators)

    if len(elevator["destinos"]) >= elevator["capacidad"]:
        return

    # bloquear array para todos los demás
    elevator["destinos"].append(person["destino"])
    person["elevator"] = elevator
    removePersonFromCell(person, person["piso"], peoplePerCell)
    # desbloquear array para todos los demás
    
    # subirAlElevador()

    while person["piso"] != person["destino"]:
        person["piso"] = elevator["pisoActual"]
        time.sleep(delay)

    # bajarDelElevador()

    person["elevator"] = None
