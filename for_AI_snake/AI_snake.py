from AI_constans import *
import numpy as np
import pygame
from enum import Enum
from collections import namedtuple
import random
from human_snake import draw_field

# вместо is_collision я могу использовать game_field.snake.alive


class Fruit:
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

class Snake:
    def __init__(self, x, y, gamefield):
        self.tail = [(x - 1, y), (x - 2, y)]
        self.head = (x, y)
        self.speed = (1, 0)
        self.new_speed = (1, 0)
        self.alive = True
        self.step = 0
        self.gamefield = gamefield

    def move(self, fruit_coords):
        """ Отвечает за перемещение змеи
        fruit_coords - положение фрукта на поле
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
                    if fruit_coords != (x + Vx, y + Vy):
                        self.tail.pop(0)
                    else:
                        self.gamefield.new_fruit()
                    self.tail.append(self.head)
                    self.head = (x + Vx, y + Vy)
                    if self.new_speed != (-Vx, -Vy):
                        self.speed = self.new_speed
                
    def up(self):
        self.new_speed = (0, -1)

    def down(self):
        self.new_speed = (0, 1)

    def left(self):
        self.new_speed = (-1, 0)
            
    def right(self):
        self.new_speed = (1, 0)

    def get_pos(self):
        """ Возвращает положения частей хвоста и головы"""
        return (self.tail, self.head)

    def get_step(self):
        return self.step


class Game:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.display = pygame.display.set_mode((2 * WIDTH, HEIGHT))
        self.GAME_RUNNING = True
        # field init:
        self.score = 0
        self.snake = Snake(FIELD_SIZE_W // 2, FIELD_SIZE_H // 2, self)
        self.fruit = Fruit(*self.snake.get_pos())
        self.screen = pygame.Surface((WIDTH, HEIGHT - BAR_HEIGHT))
        self.interf = pygame.Surface((WIDTH, BAR_HEIGHT))

    def update(self):
        self.snake.move(self.fruit.get_pos())
        self.screen.fill((0, 0, 0))
        self.screen.blit(draw_field(
            self.screen, *self.snake.get_pos(), 
            self.fruit.get_pos(), self.snake.get_step()
            ), (0, 0))
        self.interf.fill((0, 0, 0))

    def new_fruit(self):
        self.fruit = Fruit(*self.snake.get_pos())

    def snake_down(self):
        self.snake.down()

    def snake_up(self):
        self.snake.up()

    def snake_left(self):
        self.snake.left()

    def snake_right(self):
        self.snake.right()

    def mainloop(self, fields):
        self.display = pygame.display.set_mode((len(fields) * WIDTH, HEIGHT))

        while self.GAME_RUNNING:
            #print(game_field.snake.head)
            self.clock.tick(FPS)
            self.display.fill((0, 0, 0))
            self.keys_loop()
            self.update()
            self.display.blit(self.screen, (0, BAR_HEIGHT))
            self.display.blit(self.interf, (0, 0))
            pygame.display.flip()

    def keys_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.GAME_RUNNING = False 
            # для теста:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.snake_up()
                if event.key == pygame.K_DOWN:
                    self.snake_down()
                if event.key == pygame.K_LEFT:
                    self.snake_left()                        
                if event.key == pygame.K_RIGHT:
                    self.snake_right()

def main():
    Game().mainloop(["AI"])

if __name__ == "__main__":
    pygame.init()
    main()
    pygame.quit()