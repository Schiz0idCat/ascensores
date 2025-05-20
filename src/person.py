import pygame
from config import colors

def crear_persona(destino, x, y):
    return {
        "destino": destino,
        "x": x,
        "y": y,
        "en_ascensor": False
    }


def dibujar_persona(persona, screen):
    pygame.draw.circle(screen, colors.VERDE, (persona["x"], persona["y"]), 20)
    font = pygame.font.SysFont(None, 24)
    texto = font.render(str(persona["destino"]), True, colors.AZUL)
    screen.blit(texto, (persona["x"] - 8, persona["y"] - 12))

