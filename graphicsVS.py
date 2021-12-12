import pygame
import numpy as np
from constans import *


def draw_field_VSmod(surf, gamefield):
    """ Функция рисует поле.
    Первоначльно она должна нарисовать темное поле
    Исходя из массива надо нарисовать квадратики в клеточках: 
    surf - Поле на котором надо нарисовать.
    snake_tail - массив координат частей хвоста
    snake_head - координаты головы
    fruit - координаты фрукта
    step - номер шага змеи. По факту является степенью завершения змеей шага на 1 кл
    Фрукт - красный (занимает 80% ширины и высоты клетки)
    Змея - цветастая (занимает 80% ширины и высоты клетки)
    Голова - Синяя (занимает 100% ширины и высоты клетки)
    Также для каждой части змеи надо сделать соединение между двумя клеточками -
    Салатовая, например(занимает 80% ширины или высоты клетки)
    """
    for fruit in gamefield.fruits:
        (x_0, y_0) = tuple(fruit)
        x_0 *= CELL_SIDE
        y_0 *= CELL_SIDE

    for item in gamefield.walls:
        x, y = tuple(item)
        x *= CELL_SIDE
        y *= CELL_SIDE
        pygame.draw.rect(surf, GRAY, [x, y, CELL_SIDE, CELL_SIDE])

    for snake in gamefield.snakes:
        step, snake_head, snake_tail = tuple(snake)
        pygame.draw.rect(surf, RED, (x_0, y_0, CELL_SIDE, CELL_SIDE))
        k = 0.5 * (1 - WIDTH_OF_TAIL)
        (x_0, y_0) = snake_head
        (x, y) = snake_tail[-1]
        if int(abs(x - x_0) + abs(y - y_0)) == 1:
            x_0 += step / FRAMES_PER_STEP * (x_0 - x)
            y_0 += step / FRAMES_PER_STEP * (y_0 - y)
        pygame.draw.rect(surf, BLUE, (int(x_0 * CELL_SIDE), int(y_0 * CELL_SIDE), CELL_SIDE, CELL_SIDE))
        for i in range(len(snake_tail)):
            (x, y) = snake_tail[-i - 1]
            if int(abs(x - x_0) + abs(y - y_0)) == 1:
                if i == len(snake_tail) - 1:
                    x += step / FRAMES_PER_STEP * (x_0 - x)
                    y += step / FRAMES_PER_STEP * (y_0 - y)
                pygame.draw.rect(surf, SNAKE_COLORS[i % len(SNAKE_COLORS)], (
                    int((min(x, x_0) + k) * CELL_SIDE),
                    int((min(y, y_0) + k) * CELL_SIDE),
                    int(CELL_SIDE * (1 + abs(x - x_0) - 2 * k)),
                    int(CELL_SIDE * (1 + abs(y - y_0) - 2 * k))
                ))
            (x_0, y_0) = (x, y)
        x += step / FRAMES_PER_STEP * (x_0 - x)
        y += step / FRAMES_PER_STEP * (y_0 - y)
        return surf

def draw_interface(surf, score):
    """ Полоса в верху экрана, на которой выводится счет
    score - счет
    Возващает холст на котрый добавлен счет
    """
    font = pygame.font.SysFont(TEXT_FONT, 50)
    text = font.render(str(score), True, BLACK)
    text_rect = text.get_rect()
    surf_rect = surf.get_rect()
    surf.blit(text, (0.5 * (surf_rect.width - text_rect.width), 0.5 * (surf_rect.height - text_rect.height)))
    return surf

if __name__ == "__main__":
    print("This is not main file")