import pygame


# makeMatrix(rows, columns)
# Retorna un diccionario con los valores proppios de una matriz (imita un struct).
#
# Parámetros:
#  - rows (int): cantidad de rows hacia arriba.
#  - columns (int): cantidad de columns hacia la derecha.
#  - cellSize (int): tamaño, en píxeles, de las celdas de la matriz.
def makeMatrix(rows, columns, cellSize):
    return {
        "rows": rows,
        "columns": columns,
        "cellSize": cellSize
    }


# drawMatrix(screen, cellSize, color, matrix)
# Dibuja una matriz en pantalla, según sus características (desde la esquina inferior izquierda).
#
# Parámetros:
#  - screen (pygame.surface.Surface): el frame donde se dibujará.
#  - color (tuple(int, int, int)): color de la matriz (RGB).
#  - matrix (dict): diccionario retornado por makeMatrix.
def drawMatrix(screen, color, matrix):
    _, height = screen.get_size()

    rows = matrix["rows"]
    columns = matrix["columns"]
    cellSize = matrix["cellSize"]

    for row in range(rows):
        y = height - (row + 1) * cellSize
        for col in range(columns):
            x = col * cellSize
            rect = pygame.Rect(x, y, cellSize, cellSize)
            pygame.draw.rect(screen, color, rect, 1)


# drawVerticalCount(screen, coords, matrix, color)
# Dibuja una secuencia numérica vertical (contador) dentro de una columna de la matriz,
# útil para marcar pisos.
#
# Parámetros:
#  - screen (pygame.surface.Surface): frame donde se dibujará el texto.
#  - coords (tuple): una tupla de dos elementos:
#       - coordenadas (tuple(int, int)): coordenadas iniciales (columna, fila).
#       - y final (int): fila final hasta donde se dibujará el contador.
#  - matrix (dict): diccionario con los datos de la grilla (como el retornado por makeMatrix).
#  - color (tuple): color del texto en formato RGB.
def drawVerticalCount(screen, coords, matrix, color):
    rows = matrix["rows"]
    cellSize = matrix["cellSize"]

    (startX, startY), finalY = coords

    # Validamos límites
    if finalY is None or finalY >= rows:
        finalY = rows - 1
    startY = max(0, min(startY, finalY))

    font = pygame.font.SysFont(None, cellSize // 2)

    count = 0
    _, height = screen.get_size()

    for row in range(startY, finalY + 1):
        x = startX * cellSize
        y = height - (row + 1) * cellSize

        textSurface = font.render(str(count), True, color)
        textRect = textSurface.get_rect(center=(x + cellSize // 2, y + cellSize // 2))

        screen.blit(textSurface, textRect)

        count += 1
