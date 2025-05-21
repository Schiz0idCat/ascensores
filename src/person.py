import pygame
from config.settings import BUILDING


# makePerson(destino, piso, color)
# Crea un diccionario que representa a una persona con destino, piso actual y color.
#
# Parámetros:
#  - destino (int): piso al que la persona quiere ir.
#  - piso (int): piso en el que se encuentra actualmente la persona.
#  - color (tuple): color RGB para dibujar a la persona.
def makePerson(destino, piso, color):
    return {
        "destino": destino,
        "piso": piso,
        "color": color
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
    x = BUILDING["COORD"][0] + BUILDING["COLUMNAS"]
    y = persona["piso"]
    maxPorCelda = 1  # o el máximo que quieras permitir en una celda

    # Buscar celda válida para esta persona
    while True:
        # si la celda nunca ha sido ocupada
        if (x, y) not in personasPorCelda:
            personasPorCelda[(x, y)] = [] # se genera un registro para ella

        # Si ya está la persona en esta celda, no seguimos buscandole celda
        if persona in personasPorCelda[(x, y)]:
            break

        # Si no está en la celda y cabe en esta, agregamos a la persona
        if len(personasPorCelda[(x, y)]) < maxPorCelda:
            personasPorCelda[(x, y)].append(persona)
            break

        # Si no hay espacio, probamos siguiente celda a la derecha
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

