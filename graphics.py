import pygame
import numpy as np
from constans import *



class Button():
    def __init__(self, text, x, y, w, h) -> None:
        """ Класс кнопка. При создании получает входные:
        text - надпись на кнопке
        x, y - положение кнопки
        w, h - ширина и высота кнопки
        """
        self.text = text
        font = pygame.font.SysFont(TEXT_FONT, 50)
        self.t = font.render(text, True, BLACK)
        self.width = w
        self.height = h
        self.x = x
        self.y = y
        self.active = 0
        self.color = ORANGE
        self.act_color = DARK_ORANGE
        self.surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

    def check_pressed(self, x, y):
        """ Функция проверяет попадает ли мышь в прямоугольник 
        данной кнопки и возвращает соответствующее булевое значение"""
        if (abs(self.x - x) <= 0.5 * self.width and
            abs(self.y - y) <= 0.5 * self.height
            ):
            self.active = True
        else:
            self.active = False
        return self.active

    def draw_button(self, display):
        """ Отрисовывает кнопку на данном surf 
        По собственным координатам
        Должна менять цвет или выделяться при наведении"""
        col = self.color
        if self.active:
            col = self.act_color
        text = self.t
        rect = text.get_rect()
        pygame.draw.rect(display, col, (self.x - 0.5 * self.width, self.y - 0.5 * self.height, self.width, self.height))
        display.blit(text, (self.x - 0.5 * rect.width, self.y - 0.5 * rect.height))

def draw_start_menu(buttons, display):
    """ На стартовом экране Не должно быть видно будущего поля.
    На дисплей должно выводиться Меню с кнопками типа Button:
    Эти кнопки лежат в массиве buttons
    На задний план потом можно наложить принтскрин из игры
    Меню неподвижно, так что достаточно сделать правильную реализацию
    """
    for button in buttons:
        button.draw_button(display)

def draw_field(surf, snake_tail, snake_head, fruit, step):
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
    (x_0, y_0) = fruit
    x_0 *= CELL_SIDE
    y_0 *= CELL_SIDE
    pygame.draw.rect(surf, RED, (x_0, y_0, CELL_SIDE, CELL_SIDE))
    k = 0.5 * (1 - WIDTH_OF_TAIL)
    (x_0, y_0) = snake_head
    (x, y) = snake_tail[-1]
    x_0 += step / FRAMES_PER_STEP * (x_0 - x)
    y_0 += step / FRAMES_PER_STEP * (y_0 - y)
    pygame.draw.rect(surf, BLUE, (int(x_0 * CELL_SIDE), int(y_0 * CELL_SIDE), CELL_SIDE, CELL_SIDE))
    for i in range(len(snake_tail) - 1):
        (x, y) = snake_tail[-i - 1]
        pygame.draw.rect(surf, SNAKE_COLORS[i % len(SNAKE_COLORS)], (
            int((min(x, x_0) + k) * CELL_SIDE),
            int((min(y, y_0) + k) * CELL_SIDE),
            int(CELL_SIDE * (1 + abs(x - x_0) - 2 * k)),
            int(CELL_SIDE * (1 + abs(y - y_0) - 2 * k))
            ))
        (x_0, y_0) = (x, y)
    (x, y) = snake_tail[0]
    x += step / FRAMES_PER_STEP * (x_0 - x)
    y += step / FRAMES_PER_STEP * (y_0 - y)
    pygame.draw.rect(surf, SNAKE_COLORS[(len(snake_tail) - 1) % len(SNAKE_COLORS)], (
        int((min(x, x_0) + k) * CELL_SIDE),
        int((min(y, y_0) + k) * CELL_SIDE),
        int(CELL_SIDE * (1 + abs(x - x_0) - 2 * k)),
        int(CELL_SIDE * (1 + abs(y - y_0) - 2 * k))
        ))
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

def draw_text(text, size, x, y, colour, surf):
    """ Функция располагает текст на заданном холсте
    ОПОРНОЙ ТОЧКОЙ ЯВЛЯЕТСЯ СЕРЕДИНА ВЕРХА ТЕКСТА
    text: строка, вывод которой предполагается
    size: размер шрифта в пикселях
    x, y: положение опорной точки текста
    colour: цвет текста
    surf: холст, на который пишется
    """
    font = pygame.font.SysFont(TEXT_FONT, size)
    text_surface = font.render(text, True, colour)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

if __name__ == "__main__":
    print("This is not main file")