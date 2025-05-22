import pygame


# makeBuilding(pisos, columnas, ascensores)
# Retorna un diccionario con los valores propios de un edificio (imita un struct)
#
# Parámetros:
#  - floors (int): cantidad de pisos del edificio (alto)
#  - columns (int): cantidad de columnas del edificio (ancho)
#  - lenElevators (int): cantidad de ascensores del edificio
def makeBuilding(floors, columns, lenElevators):
    return {
        "floors": floors,
        "cols": columns,
        "lenElevators": lenElevators
    }


# drawBuilding(screen, cellSize, coords, edificio, color, thickness)
# Dibuja el edificio en pantalla, según sus características y una posición base.
#
# Parámetros:
#  - screen (pygame.surface.Surface,): el frame donde se dibujará
#  - cellSize (int): tamaño de cada celda de la matriz (en píxeles)
#  - coords (tuple(int, int)): coordenadas (x, y) donde empieza el dibujo (desde la esquina inferior izquierda)
#  - building (dict): diccionario retornado por makeBuilding, con 'pisos', 'columnas' y 'ascensores'
#  - color (tuple(int, int, int)): color del borde del edificio (RGB)
#  - thickness (int): grosor de las líneas
def drawBuilding(screen, cellSize, coords, building, color, thickness):
    # desempaquetamiento por legibilidad
    x, y = coords
    ancho = building["cols"]
    alto = building["floors"]

    screen_height = screen.get_height()

    # Coordenadas en relación con las celdas de la matriz
    px = x * cellSize
    py = screen_height - (y + alto) * cellSize
    width = ancho * cellSize
    height = alto * cellSize

    # Dibujar contorno del edificio
    rect = pygame.Rect(px, py, width, height)
    pygame.draw.rect(screen, color, rect, thickness)

    # Líneas de los pisos
    for i in range(1, alto):
        piso_y = py + i * cellSize
        pygame.draw.line(screen, color, (px, piso_y), (px + width, piso_y), thickness)

