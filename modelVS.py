from constans import *


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

    def move(self, fruit, dangers):
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
            if not(0 <= (x + Vx) < FIELD_SIZE_W and 0 <= (y + Vy) < FIELD_SIZE_H):
                self.speed = (0, 0)
                self.alive = False
            else:
                for part in dangers:
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
                
    def up(self):
        """ Попытка поворта наверх"""
        self.direction = (0, -1)

    def down(self):
        """ Попытка поворта вниз"""
        self.direction = (0, 1)

    def left(self):
        """ Попытка поворта налево"""
        self.direction = (-1, 0)
            
    def right(self):
        """ Попытка поворта направо"""
        self.direction = (1, 0)

    def get_pos(self):
        """ Возвращает положения частей хвоста и головы"""
        return (self.tail, self.head)

    def get_step(self):
        """ Возвращает степень законченности перехода"""
        return self.step