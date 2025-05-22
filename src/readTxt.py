# leetTxt(path)
# lee el txt con configuraciones del proyecto 
#
# Parámetros:
#  - path (str): path del txt a leer 
def leerTxt(path):
    with open(path, 'r') as f:
        # Leer los primeros 4 valores, cada uno en una línea
        elevators = int(f.readline().strip())
        elevatorCapacity = int(f.readline().strip())
        peoplePerDay = int(f.readline().strip())
        peoplePerTick = int(f.readline().strip())

        # Leer los 10 tiempos por piso
        floorTime = [int(f.readline().strip()) for _ in range(10)]

    return {
        "elevators": elevators,
        "elevatorCapacity": elevatorCapacity,
        "peoplePerDay": peoplePerDay,
        "peoplePerTick": peoplePerTick,
        "floorTime": floorTime
    }
