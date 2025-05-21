import sys
import threading
import pygame
import random
from config import colors
from config.settings import FRAME, GRID, BUILDING
from src import grid, building, elevator, person


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

    # Crear ascensores y hilos
    ascensores = []
    hilos = []

    for i in range(edificio["ascensores"]):
        asc = elevator.makeElevator(
            columna = i,
            pisoActual = 0,
            maxPisos = edificio["pisos"],
            destinos = []
        )
        ascensores.append(asc)

        hilo = threading.Thread(target=elevator.goto, args=(asc, 1.0), daemon=True)
        hilo.start()
        hilos.append(hilo)

    # personasPorCelda = {
    #     (Xcoord, Ycoord): [personas] // en la celda (x, y), están tales personas 
    # }
    personasPorCelda = {}
    personas = []
    for i in range(5):
        destino = random.randint(1, edificio["pisos"] - 1)  # pisos destino entre 1 y N-1
        piso = 0 # parte en el piso 0
        p = person.makePerson(destino, piso, colors.rand())
        personas.append(p)

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
            elevator.drawElevator(screen, asc, matriz["cellSize"], colors.RED, colors.GREEN)


        for persona in personas:
            person.drawPerson(screen, persona, matriz["cellSize"], personasPorCelda, persona["color"])

        pygame.display.flip()
        clock.tick(FRAME["FPS"])

    pygame.quit()
    sys.exit()
