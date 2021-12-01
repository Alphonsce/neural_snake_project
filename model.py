from constans import *
import random



class Fruit:
    """ Тип фрукта"""
    def __init__(self, snakepose, snakehead, walls):
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
            for item in walls:
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
        self.tail = [(x-1, y), (x-2, y)]
        self.head = (x, y)
        self.speed = (1, 0)
        self.direction = Direction.RIGHT
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
            Vx, Vy = self.speed
            if self.direction.value != (-Vx, -Vy):
                self.speed = self.direction.value
                Vx, Vy = self.speed
            self.step = 0
            x, y = self.head 
            x_new, y_new = self.gamefield.rule(self, x + Vx, y + Vy)
            if self.alive:
                self.tail.append(self.head)
                self.head = (x_new, y_new)
                if fruit != (x_new, y_new):
                    self.tail.pop(0)
                else:
                    self.gamefield.new_fruit()

    def standart_rule(self, x_new, y_new):
        if not(0 <= x_new < FIELD_SIZE_W and 0 <= y_new < FIELD_SIZE_H):
            self.speed = (0, 0)
            self.alive = False
        else:
            for part in self.tail[1:]:
                if part == (x_new, y_new):
                    self.speed = (0, 0)
                    self.alive = False
        return x_new, y_new

    def inf_field(self, x_new, y_new):
        x_new %= FIELD_SIZE_W 
        y_new %= FIELD_SIZE_H
        for part in self.tail[1:]:
            if part == (x_new, y_new):
                self.speed = (0, 0)
                self.alive = False
        return x_new, y_new

    def walls(self, x_new, y_new):
        x_new %= FIELD_SIZE_W 
        y_new %= FIELD_SIZE_H
        for part in self.tail[1:]:
            if part == (x_new, y_new):
                self.speed = (0, 0)
                self.alive = False
        for part in self.gamefield.walls:
            if part == (x_new, y_new):
                self.speed = (0, 0)
                self.alive = False
        return x_new, y_new

    def get_pos(self):
        """ Возвращает положения частей хвоста и головы"""
        return (self.tail, self.head)

    def get_step(self):
        """ Возвращает степень законченности перехода"""
        return self.step


if __name__ == "__main__":
    print("This is not main file")