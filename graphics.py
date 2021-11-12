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
        self.t = font.render(text, True, BLACK)
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
        text = font.render(self.text, True, c)
        text_rect = text.get_rect(center = (WIDTH // 2, self.h))
        screen.blit(text, text_rect)

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

def draw_field(cells, surf):
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
    
    return surf

def draw_interface():
    """ Полоса в верху экрана на которой выводится счет"""
    pass #FIXME

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