import pygame

from constans import *


def draw_field_VSmod(surf, gamefield):
    """ Функция рисует поле.
    Первоначльно она должна нарисовать темное поле
    Исходя из массива надо нарисовать квадратики в клеточках: 
    surf - Поле на котором надо нарисовать.
    gamefield - игра из которой берутся данные для отрисовки
    Фрукт - красный (занимает 100% ширины и высоты клетки)
    Змея - цветастая (занимает 80% ширины и высоты клетки)
    Голова - Синяя (занимает 100% ширины и высоты клетки)
    Стена - Серая (занимает 100% ширины и высоты клетки)

    """
    for fruit in gamefield.fruits:
        (x_0, y_0) = tuple(fruit)
        x_0 *= CELL_SIDE
        y_0 *= CELL_SIDE
        pygame.draw.rect(surf, RED, (x_0, y_0, CELL_SIDE, CELL_SIDE))

    for item in gamefield.walls:
        x, y = tuple(item)
        x *= CELL_SIDE
        y *= CELL_SIDE
        pygame.draw.rect(surf, GRAY, [x, y, CELL_SIDE, CELL_SIDE])

    for snake in gamefield.snakes:
        step, snake_head, snake_tail = tuple(snake)
        k = 0.5 * (1 - WIDTH_OF_TAIL)
        (x_0, y_0) = snake_head
        (x, y) = tuple(snake_tail[-1])
        x_0 += step / FRAMES_PER_STEP * (x_0 - x)
        y_0 += step / FRAMES_PER_STEP * (y_0 - y)
        pygame.draw.rect(surf, BLUE, (int(x_0 * CELL_SIDE), int(y_0 * CELL_SIDE), CELL_SIDE, CELL_SIDE))
        for i in range(len(snake_tail)):
            (x, y) = tuple(snake_tail[-i - 1])
            if i == len(snake_tail) - 1:
                x += step / FRAMES_PER_STEP * (x_0 - x)
                y += step / FRAMES_PER_STEP * (y_0 - y)
            # SNAKE_COLORS[i % len(SNAKE_COLORS)]
            pygame.draw.rect(surf, BLUE, (
                int((min(x, x_0) + k) * CELL_SIDE),
                int((min(y, y_0) + k) * CELL_SIDE),
                int(CELL_SIDE * (1 + abs(x - x_0) - 2 * k)),
                int(CELL_SIDE * (1 + abs(y - y_0) - 2 * k))
            ))
            (x_0, y_0) = (x, y)
        x += step / FRAMES_PER_STEP * (x_0 - x)
        y += step / FRAMES_PER_STEP * (y_0 - y)
    return surf


if __name__ == "__main__":
    print("This is not main file")
