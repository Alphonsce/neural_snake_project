from enum import Enum

GRAY = (150, 150, 150)
GREEN = (0, 200, 0)
WHITE = (255, 255, 255)
RED = (250, 0, 0)
BLUE = (0, 0, 250)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

# Стиль текста
TEXT_FONT = "arial"

WIDTH = 1500
HEIGHT = 800

FPS = 30
TIME_STEP = 200

class Cell(Enum):
    Empty = 0
    Snake = 1
    Snake_head = 2
    Fruit = 3