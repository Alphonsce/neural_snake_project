from enum import Enum

# константы обучения:
# LR - learning rate -отвечает за размер шага при градиентном спуске

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.0015      # learning rate, отвечает за размер шага в градиентном спуске

GAMMA = 0.9     # параметр, регулирующий обучение с подкреплением
STARTING_EPSILON = 80     # параметр, отвечающий за случайность принятых агентом решений

WAITING_CONSTANT = 500      # отвечает за то как долго мы готовы ждать конца, когда агент циклит одно движение
#---------------

GRAY = (150, 150, 150)
GREEN = (0, 200, 0)
WHITE = (255, 255, 255)
RED = (250, 0, 0)
BLUE = (0, 0, 250)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
ORANGE = 0xBE5504
DARK_ORANGE = 0x7A3803
SNAKE_COLORS = [BLUE]

TEXT_FONT = "arial" # Стиль текста

# параметры игрового поля. Изменение не рекомендованно
WIDTH = 750 
HEIGHT = 800
BAR_HEIGHT = 50
CELL_SIDE = 30
# ширина и высота игрового поля в клеточках
FIELD_SIZE_W = int((WIDTH) // CELL_SIDE)        # 25, максимально, когда змея жива: 24
FIELD_SIZE_H = int((HEIGHT - BAR_HEIGHT) // CELL_SIDE)      # 25, максимально, когда змея жива: 24

WIDTH_OF_TAIL = 0.8 #коэффициент толщины для рисовки хвоста
 
#Количество обработок в секунду
FPS = 60
# По факту задает скорость змеи. V * FRAMES_PER_STEP = FPS
FRAMES_PER_STEP = 5


# Пока что не используемый нами блок
class Cell(Enum):
    Empty = 0
    Snake = 1
    Snake_head = 2
    Fruit = 3


class Direction(Enum):
    def __eq__(self, other):
        if self.value == other.value:
            return True
        return False

    RIGHT = (1, 0)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    UP = (0, -1)
