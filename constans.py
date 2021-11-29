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
SNAKE_COLORS = [BLUE, GREEN, YELLOW]

# Константы для названия
NAME_COLOR = YELLOW
NAME_OF_GAME = 'Змейка'

TEXT_FONT = "arial" # Стиль текста

# параметры игрового поля. Изменение не рекомендованно
WIDTH = 750 
HEIGHT = 800
BAR_HEIGHT = 50
CELL_SIDE = 30
# ширина и высота игрового поля в клеточках
FIELD_SIZE_W = int((WIDTH) // CELL_SIDE)
FIELD_SIZE_H = int((HEIGHT - BAR_HEIGHT) // CELL_SIDE)

WIDTH_OF_TAIL = 0.8 #коэффициент толщины для рисовки хвоста
 
#Количество обработок в секунду
FPS = 60
# По факту задает скорость змеи. V * FRAMES_PER_STEP = FPS
FRAMES_PER_STEP = 6

class Direction(Enum):
    def __eq__(self, other):
        if self.value == other.value:
            return True
        return False

    RIGHT = (1, 0)
    LEFT = (-1, 0)
    UP = (0, -1)
    DOWN = (0, 1)
