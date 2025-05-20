def leerTxt(path):
    with open(path, 'r') as f:
        # Leer los primeros 4 valores, cada uno en una línea
        ascensores = int(f.readline().strip())
        maxPersonasAscensor = int(f.readline().strip())
        personasPorDia = int(f.readline().strip())
        personasPorCiclo = int(f.readline().strip())

        # Leer los 10 tiempos por piso
        tiempoPorPiso = [int(f.readline().strip()) for _ in range(10)]

    return {
        "ascensores": ascensores,
        "maxPersonasAscensor": maxPersonasAscensor,
        "personasPorDia": personasPorDia,
        "personasPorCiclo": personasPorCiclo,
        "tiempoPorPiso": tiempoPorPiso
    }
