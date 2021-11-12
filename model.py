from constans import *
import random


class Fruit():
    def __init__(self, snakepose, snakehead):
        not_founded = True
        while not_founded:
            not_founded = False
            self.pos = (random.randint(0, FIELD_SIZE_W - 1), random.randint(0, FIELD_SIZE_H - 1))
            for item in snakepose:
                if snakepose == self.pos:
                    not_founded = True
            if snakehead == self.pos:
                not_founded = True
    
    def get_pos(self):
        return self.pos

class Snake():
    def __init__(self, x, y):
        self.taile = []
        self.head = (x, y)
        self.speed = (1, 0)
        self.alive = True

    def move(self, fruit):
        """ Отвечает за перемещение змеи
        fruit - положение фрукта на поле
        """
        x, y = self.head 
        Vx, Vy = self.speed
        if not( 0 <= (x + Vx) < FIELD_SIZE_W and 0 <= (y + Vy) < FIELD_SIZE_H):
            self.speed = (0, 0)
            self.alive = False
            print(x, y)
        else:
            for part in self.taile[1:]:
                if part == (x + Vx, y + Vy):
                    self.speed = (0, 0)
                    self.alive = False
            if self.alive:
                if fruit != (x + Vx, y + Vy):
                    self.taile.pop(0)
                self.taile.append(self.head)
                self.head = (x + Vx, y + Vy)
                
    def rot_right(self):
        """ Поворот змеи направо"""
        Vx, Vy = self.speed
        self.speed = (-Vy, Vx)

    def rot_left(self):
        """ Поворот змеи налево"""
        Vx, Vy = self.speed
        self.speed = (Vy, -Vx)

    def get_pos(self):
        """ Возвращает положения частей хвоста и головы"""
        return (self.taile, self.head)


if __name__ == "__main__":
    print("This is not main file")