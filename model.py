from constans import *



class Fruit():
    pass

class Snake():
    def __init__(self, x, y):
        self.taile = []
        self.head = (x, y)
        self.speed = (1, 0)

    def move(self):
        pass

    def rot_right(self):
        Vx, Vy = self.speed
        self.speed = (-Vy, Vx)

    def rot_left(self):
        Vx, Vy = self.speed
        self.speed = (Vy, -Vx)

if __name__ == "__main__":
    print("This is not main file")