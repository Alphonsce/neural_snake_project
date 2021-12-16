import random

from constans import *


class FruitVS:
    """ Тип фрукта"""
    def __init__(self, game):
        """Создание фрукта. На вход передается 
        game - игровое поле 
        """
        self.game = game
        self.new_fruit()

    def new_fruit(self):
        """ Создание фрукта перебором возможных координат
        """
        not_founded = True
        while not_founded:
            not_founded = False
            x, y = (random.randint(FIELD_SIZE_W, self.game.field_size_w - FIELD_SIZE_W - 1),
                random.randint(FIELD_SIZE_H, self.game.field_size_h - FIELD_SIZE_H - 1))
            if self.game.cell[x][y].value != 0:
                not_founded = True
        self.pos = x, y
        self.game.cell[x][y] = Cell.Fruit
    
    def get_pos(self):
        """ Функция возвращает положение фрукта"""
        return self.pos 

class SnakeVS:
    """ Класс змея. Является основным игроком"""
    def __init__(self, x, y, game, gamer):
        """ Создание змеи 
        x, y - начальные координаты головы 
        game - игровое поле, в котором змейка перемещается
        gamer - игрок, управляющий змеей
        """
        self.tail = [(x-2, y), (x-1, y)]
        self.head = (x, y)
        self.speed = (1, 0)
        self.direction = Direction.RIGHT
        self.alive = True
        self.step = 0
        self.game = game
        self.gamer = gamer

    def move(self):
        """ Отвечает за перемещение змеи
        Положение объектов считывается из self.game
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
            cell = self.game.cell[x+Vx][y+Vy]
            if cell.value == 1:
                self.gamer.death()
                
            elif cell.value == 2:
                self.gamer.death()
                for gam in self.game.gamers:
                    if gam.snake.head == (x + Vx, y + Vy):
                        gam.death()
            elif cell.value == 4:
                self.gamer.death()

            if self.alive:
                self.tail.append(self.head)
                self.head = (x + Vx, y + Vy)
                self.game.cell[x][y] = Cell.Snake
                self.game.cell[x+Vx][y+Vy] = Cell.Head
                if cell.value == 3:
                    for fruit in self.game.fruits:
                        if fruit.pos == (x + Vx, y + Vy):
                            fruit.new_fruit()
                else:
                    x, y = self.tail.pop(0)
                    self.game.cell[x][y] = Cell.Nothing

                

    def get_pos(self):
        """ Возвращает положения частей хвоста и головы"""
        return (self.tail, self.head)

    def get_step(self):
        """ Возвращает степень законченности перехода"""
        return self.step
