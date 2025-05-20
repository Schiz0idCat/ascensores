import random

def rand(min=50, max=200):
    return (random.randint(min, max), random.randint(min, max), random.randint(min, max))

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (80, 80, 80)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
