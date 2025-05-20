import sys
import pygame
from config import colors
from config.settings import FRAME, GRID, BUILDING
from src import grid, building, elevator


if __name__ == "__main__":
    # pygame cosas
    pygame.init()
    screen = pygame.display.set_mode(FRAME["SET_RESOLUTION"])
    pygame.display.set_caption(FRAME["TITLE"])
    clock = pygame.time.Clock()

    # Se calcula el tamaño de las celdas con base en la cantidad de filas
    screen_width, screen_height = screen.get_size()
    cellSize = screen_height // GRID["ROWS"]
    columnas = GRID["COLS"] if GRID["COLS"] >= 0 else screen_width // cellSize

    # Se crea la matriz que se dibuja de fondo
    matriz = grid.makeMatrix(
        filas = GRID["ROWS"],
        columnas = columnas,
        cellSize = cellSize
    )

    # Se crea el edificio
    edificio = building.makeBuilding(
        pisos = BUILDING["PISOS"],
        columnas = BUILDING["COLUMNAS"],
        ascensores =  BUILDING["ASCENSORES"]
    )

    # Se crean los ascensores
    ascensores = []
    for i in range(edificio["ascensores"]):
        asc = elevator.crear_ascensor(
            columna = i,
            pisoActual = 0,
            maxPisos = edificio["pisos"]
        )
        ascensores.append(asc)

    # Bucle principal
    running = True
    while running:
        screen.fill(colors.BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        grid.drawMatrix(screen, colors.GRAY, matriz)
        grid.drawVerticalCount(screen, BUILDING["FLOORS_COUNT"], matriz, colors.WHITE)
        building.drawBuilding(screen, matriz["cellSize"], BUILDING["COORD"], edificio, colors.WHITE, BUILDING["THICKNESS"])
        for asc in ascensores:
            elevator.dibujar_ascensor(screen, asc, matriz["cellSize"], colors.RED, colors.GREEN)

        pygame.display.flip()
        clock.tick(FRAME["FPS"])

    pygame.quit()
    sys.exit()
