import pygame


# makeBuilding(pisos, columnas, ascensores)
# Retorna un diccionario con los valores propios de un edificio (imita un struct)
#
# Parámetros:
#  - pisos (int): cantidad de pisos del edificio (alto)
#  - columnas (int): cantidad de columnas del edificio (ancho)
#  - ascensores (int): cantidad de ascensores del edificio
def makeBuilding(pisos: int, columnas: int, ascensores: int):
    return {
        "pisos": pisos,
        "columnas": columnas,
        "ascensores": ascensores
    }


# drawBuilding(screen, cellSize, coords, edificio, color, thickness)
# Dibuja el edificio en pantalla, según sus características y una posición base.
#
# Parámetros:
#  - screen: el frame donde se dibujará
#  - cellSize: tamaño de cada celda de la matriz (en píxeles)
#  - coords: coordenadas (x, y) donde empieza el dibujo (desde la esquina inferior izquierda)
#  - edificio: diccionario retornado por makeBuilding, con 'pisos', 'columnas' y 'ascensores'
#  - color: color del borde del edificio (RGB)
#  - thickness: grosor de las líneas
def drawBuilding(screen: pygame.surface.Surface, cellSize: int, coords: tuple, edificio: dict, color: tuple, thickness: int):
    # desempaquetamiento por legibilidad
    x, y = coords
    ancho = edificio["columnas"]
    alto = edificio["pisos"]

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
