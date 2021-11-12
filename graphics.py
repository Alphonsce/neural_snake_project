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
        self.t = TEXT_FONT.render(text, True, BLACK)
        self.width = self.t.get_rect().width
        self.height = self.t.get_rect().height
        self.h = h
        self.active = 0
        self.color = ORANGE
        self.act_color = DARK_ORANGE
        self.text_rect = self.t.get_rect(center=(WIDTH // 2, self.h))
        print(self.width, self.height) 

    def check_pressed(self, x, y):
        """ Функция проверяет попадает ли мышь 
        в прямоугольник данной кнопки"""
        x, y = pygame.mouse.get_pos()
        if abs(WIDTH // 2 - x) <= self.width / 2 and np.abs(self.h - y) < self.height / 2:
            self.active = 1
        else:
            self.active = 0

    def draw_button(self):
        """ Отрисовывает кнопку
        Должна менять цвет или выделяться при наведении"""
        c = self.color
        if self.active == 1:
            c = self.act_color
        text = TEXT_FONT.render(self.text, True, c)
        text_rect = text.get_rect(center = (WIDTH // 2, self.h))
        return text, text_rect

def draw_start_menu(buttons):
    """ На стартовом экране Не должно быть видно будущего поля.
    На дисплей должно выводиться Меню с кнопками типа Button:
    SINGLE PLAYER
    PLAYER VS AI
    JUST AI
    STATICS
    EXIT

    Эти кнопки лежат в массиве buttons
    На задний план потом можно наложить принтскрин из игры
    Меню неподвижно, так что достаточно сделать правильную реализацию
    """
    pass

def draw_field(surf, snake_tail, snake_head, fruit, step):
    """ Функция рисует поле.
    Первоначльно она должна нарисовать темное поле
    Исходя из массива надо нарисовать квадратики в клеточках: 
    surf - Поле на котором надо нарисовать.
    cells - массив чисел. Соответствия устанавливаются с помощью 
    класса Cell в модуле constans
    Фрукт - красный (занимает 80% ширины и высоты клетки)
    Змея - зеленая (занимает 80% ширины и высоты клетки)
    Голова - Зеленая (занимает 100% ширины и высоты клетки)
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
    for i in range(len(snake_tail)-1):
        (x, y) = snake_tail[-i-1]
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
    pygame.draw.rect(surf, SNAKE_COLORS[i % len(SNAKE_COLORS)], (
        int((min(x, x_0) + k) * CELL_SIDE),
        int((min(y, y_0) + k) * CELL_SIDE),
        int(CELL_SIDE * (1 + abs(x - x_0) - 2 * k)),
        int(CELL_SIDE * (1 + abs(y - y_0) - 2 * k))
        ))
    return surf

def draw_interface(surf, score):
    """ Полоса в верху экрана, на которой выводится счет"""
    pass #FIXME
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