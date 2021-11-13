from constans import *
import random


class Fruit:
    """ Тип фрукта"""
    def __init__(self, snakepose, snakehead):
        """ Создание фрукта перебором возможных координат
        на вход подаются 
        snakepose - координаты частей хвоста
        snakehead - координаты головы
        """
        not_founded = True
        while not_founded:
            not_founded = False
            self.pos = (random.randint(0, FIELD_SIZE_W - 1), random.randint(0, FIELD_SIZE_H - 1))
            for item in snakepose:
                if item == self.pos:
                    not_founded = True
            if snakehead == self.pos:
                not_founded = True
    
    def get_pos(self):
        """ Функция возвращает положение фрукта"""
        return self.pos

class Snake:
    """ Класс змея. Является основным игроком"""
    def __init__(self, x, y, gamefield):
        """ Создание змеи 
        x, y - начальные координаты головы 
        gamefield - игровое поле, в котором змейка перемещается
        """
        self.tail = [(x-1, y)]
        self.head = (x, y)
        self.speed = (1, 0)
        self.new_speed = (1, 0)
        self.alive = True
        self.step = 0
        self.gamefield = gamefield

    def move(self, fruit):
        """ Отвечает за перемещение змеи
        fruit - положение фрукта на поле
        """
        if self.alive:
            self.step += 1
        if self.step >= FRAMES_PER_STEP:
            self.step = 0
            x, y = self.head 
            Vx, Vy = self.speed
            if not(0 <= (x + Vx) < FIELD_SIZE_W and 0 <= (y + Vy) < FIELD_SIZE_H):
                self.speed = (0, 0)
                self.alive = False
            else:
                for part in self.tail[1:]:
                    if part == (x + Vx, y + Vy):
                        self.speed = (0, 0)
                        self.alive = False
                if self.alive:
                    if fruit != (x + Vx, y + Vy):
                        self.tail.pop(0)
                    else:
                        self.gamefield.new_fruit()
                    self.tail.append(self.head)
                    self.head = (x + Vx, y + Vy)
                    if self.new_speed != (-Vx, -Vy):
                        self.speed = self.new_speed
                
    def up(self):
        """ Попытка поворта наверх"""
        self.new_speed = (0, -1)

    def down(self):
        """ Попытка поворта вниз"""
        self.new_speed = (0, 1)

    def left(self):
        """ Попытка поворта налево"""
        self.new_speed = (-1, 0)
            
    def right(self):
        """ Попытка поворта направо"""
        self.new_speed = (1, 0)

    def get_pos(self):
        """ Возвращает положения частей хвоста и головы"""
        return (self.tail, self.head)

    def get_step(self):
        """ Возвращает степень законченности перехода"""
        return self.step


if __name__ == "__main__":
    print("This is not main file")