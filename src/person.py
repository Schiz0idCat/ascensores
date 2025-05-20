import pygame

def makePerson(destino, color):
    return {
        "destino": destino,
        "en_ascensor": False,
        "color": color
    }


def drawPerson(screen, persona, cellSize, coord, personas_por_celda, color):
    col, row = coord

    # Recuento actual de personas en esa celda
    key = (col, row)
    count = len(personas_por_celda.get(key, []))

    # Si hay más de 4 personas, mover a la celda de la derecha
    if count >= 5:
        col += 1
        key = (col, row)
        count = len(personas_por_celda.get(key, []))

    # Añadir persona a la celda actual
    if key not in personas_por_celda:
        personas_por_celda[key] = []
    personas_por_celda[key].append(persona)

    # Recalcular posición y tamaño
    margin = 4
    radius = (cellSize - 2 * margin) // 3  # Tamaño reducido para múltiples personas
    total = len(personas_por_celda[key])
    max_in_cell = min(5, total)

    # Coordenadas base
    screen_height = screen.get_height()
    x0 = col * cellSize
    y0 = screen_height - (row + 1) * cellSize

    # Distribuir horizontalmente (alineados en fila dentro de celda)
    spacing = cellSize // max_in_cell
    index = personas_por_celda[key].index(persona)
    cx = x0 + spacing * index + spacing // 2
    cy = y0 + cellSize // 2

    # Dibujar círculo (persona)
    pygame.draw.circle(screen, color, (cx, cy), radius)
    pygame.draw.circle(screen, (0, 0, 0), (cx, cy), radius, 2)  # borde negro
