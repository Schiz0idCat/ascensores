from src import readTxt

FRAME = {
    "RESOLUTIONS": {  # Resoluciones disponibles:
        "SD": (640, 480),  # - Standard Definition (4:3)
        "QHD": (960, 540), # - (16:9)
        "HD": (1280, 720),  # - High Definition (16:9)
        "HD+": (1600, 900),  # - HD+ (16:9)
        "FHD": (1920, 1080),  # - Full HD (16:9)
    },
    "RESOLUTION": "QHD",  # Resolución seleccionada
    "FPS": 60,  # Tasa de refresco
    "TITLE": "Elevators",  # Título de la ventana
}

# Aplica la resolución deseada
FRAME["SET_RESOLUTION"] = FRAME["RESOLUTIONS"][FRAME["RESOLUTION"]]

GRID = {
    "ROWS": 12,  # Cantidad de filas
    "COLS": -1  # Cantidad de columnas (-1 para usar todo el ancho)
}

TXT = readTxt.leerTxt("./config/ascensores.txt")

BUILDING = {
    "FLOORS": 11,
    "COLS": 3,
    "ELEVATORS": TXT["elevators"],
    "COORD": (1, 0),  # Coordenadas donde se dibuja el edificio
    "THICKNESS": 2
}

# Se controla que el ancho del edificio alcanze para sus ascensores
BUILDING["COLS"] = BUILDING["ELEVATORS"] if BUILDING["COLS"] < BUILDING["ELEVATORS"] else BUILDING["COLS"]
# Coordenadas para el conteo de pisos del edificio
BUILDING["FLOORS_COUNT"] = ((BUILDING["COORD"][0] - 1, BUILDING["COORD"][1]), BUILDING["FLOORS"] - 1)
