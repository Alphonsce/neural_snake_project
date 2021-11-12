from enum import Enum

GRAY = (150, 150, 150)
GREEN = (0, 200, 0)
WHITE = (255, 255, 255)
RED = (250, 0, 0)
BLUE = (0, 0, 250)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
ORANGE = 0xBE5504
DARK_ORANGE = 0x7A3803

# Стиль текста
TEXT_FONT = "arial"

WIDTH = 750
HEIGHT = 800

BAR_HEIGHT = 50
CELL_SIDE = 30
WIDTH_OF_TAIL = 0.8 #коэффициент уменьшения для рисовки хвоста

FIELD_SIZE_W = int((WIDTH) // CELL_SIDE)
FIELD_SIZE_H = int((HEIGHT - BAR_HEIGHT) // CELL_SIDE)

FPS = 30
TIME_STEP = 200


class Cell(Enum):
    Empty = 0
    Snake = 1
    Snake_head = 2
    Fruit = 3