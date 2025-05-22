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
    columns = GRID["COLS"] if GRID["COLS"] >= 0 else screen_width // cellSize

    # Se crea la matriz que se dibuja de fondo
    matrix = grid.makeMatrix(
        rows = GRID["ROWS"],
        columns = columns,
        cellSize = cellSize
    )

    # Se crea el edificio
    tower = building.makeBuilding(
        floors = BUILDING["FLOORS"],
        columns = BUILDING["COLS"],
        lenElevators =  BUILDING["ELEVATORS"]
    )

    # Crear ascensores y hilos
    elevators = []
    thrdElevatros = []
    for i in range(tower["lenElevators"]):
        lift = elevator.makeElevator(
            column = i,
            currentFloor = 0,
            floors = tower["floors"],
            targets = []
        )
        elevators.append(lift)

        hilo = threading.Thread(target=elevator.goto, args=(lift, 1.0), daemon=True)
        hilo.start()
        thrdElevatros.append(hilo)

    # personasPorCelda = {
    #     (Xcoord, Ycoord): [personas] // en la celda (x, y), están tales personas 
    # }
    peoplePerCell = {}
    people = []
    thrdPeople = []
    for i in range(20):
        target = random.randint(1, tower["floors"] - 1)  # pisos destino entre 1 y N-1
        currentFloor = 0 # parte en el piso 0
        user = person.makePerson(
            target,
            currentFloor,
            colors.rand(),
            None
        )
        people.append(user)

        hilo = threading.Thread(target=person.goto, args=(elevators, user, peoplePerCell), daemon=True)
        hilo.start()
        thrdPeople.append(hilo)

    # Bucle principal
    running = True
    while running:
        screen.fill(colors.BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        grid.drawMatrix(screen, colors.GRAY, matrix)
        grid.drawVerticalCount(screen, BUILDING["FLOORS_COUNT"], matrix, colors.WHITE)
        building.drawBuilding(screen, matrix["cellSize"], BUILDING["COORD"], tower, colors.WHITE, BUILDING["THICKNESS"])


        for lift in elevators:
            elevator.drawElevator(screen, lift, matrix["cellSize"], colors.RED, colors.GREEN)


        for user in people:
            person.drawPerson(screen, user, matrix["cellSize"], peoplePerCell, user["color"])

        pygame.display.flip()
        clock.tick(FRAME["FPS"])

    pygame.quit()
    sys.exit()
