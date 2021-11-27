from AI_constans import *
import numpy as np
import pygame
from enum import Enum
from collections import namedtuple
import random
from human_snake import draw_field
#from agent_for_learning import Learning_Agent

# вместо is_collision я могу использовать game_field.snake.alive
# action имеет формат [straight, right, left]
# внутри AI_Game я сделаю другой метод, который будет из action делать direction и потом просто вызывать move(direction)
# как получить direction из action: [R, D, L, U] - направления по часовой, если action = [0, 1, 0] - сохраняем direction,
# если action = [1, 0, 0] - то смещаемся против часовой, если action = [0, 0, 1] - смещаемся по часовой

# reward начисляется за каждый отдельный ход, т.е. за каждую отдельный прогон mainloop_step будет назначен reward

class Fruit:
    def __init__(self, snakepose, snakehead):
        not_founded = True
        while not_founded:
            not_founded = False
            self.pos = (random.randint(0, FIELD_SIZE_W - 1), random.randint(0, FIELD_SIZE_H - 1))
            for item in snakepose:
                if item == self.pos:
                    not_founded = True
            if snakehead == self.pos:
                not_founded = True
                

class Snake:
    def __init__(self, x, y, gamefield):
        self.tail = [(x - 1, y), (x - 2, y)]
        self.head = (x, y)
        self.speed = (1, 0)
        self.alive = True
        self.step = 0
        self.gamefield = gamefield
        self.direction = Direction.RIGHT

    def move(self, fruit_coords):
        """ Отвечает за перемещение змеи
        fruit_coords - положение фрукта на поле

        Суть теперь в том, чтобы здесь делать движиние по direction,
        который мы получаем из action при помощи метода в классе AI_Game
        """

        if self.alive:
            self.step += 1
        if self.step >= FRAMES_PER_STEP:
            self.step = 0
            x, y = self.head 
            Vx, Vy = self.direction.value
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

    def get_pos(self):
        """ Возвращает положения частей хвоста и головы"""
        return (self.tail, self.head)

    def get_step(self):
        return self.step


class AI_Game:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.display = pygame.display.set_mode((WIDTH, HEIGHT))
        # field init:
        self.reset()

    def reset(self):
        '''здесь находятся все параметры для инициализации игры заново'''
        self.frame_number = 0
        self.score = 0
        self.snake = Snake(FIELD_SIZE_W // 2, FIELD_SIZE_H // 2, self)
        self.fruit = Fruit(*self.snake.get_pos())
        self.screen = pygame.Surface((WIDTH, HEIGHT - BAR_HEIGHT))

    def update_drawing(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(draw_field(
            self.screen, *self.snake.get_pos(), 
            self.fruit.pos, self.snake.get_step()
            ), (0, 0))

    def is_looped(self):
        ''' проверка на то что агент стал циклить одно движение,
        self.frame_number после собирания фрукта обновляется внутри new_fruit
        '''
        if self.frame_number > WAITING_CONSTANT * (len(self.snake.tail) + 1):
            self.snake.alive = False

    def will_be_dead(self, point):
        '''функция, которая показывает по переданной ей координате точки,
        будет ли игра проиграна, если этой точкой будет голова
        '''
        x, y = point

        # смерть об стены:
        if x >= FIELD_SIZE_W or y >= FIELD_SIZE_H:
            return True
        # смерть об хвост:
        if (x, y) in self.snake.tail:
            return True
        return False


    def direction_from_action(self, action=[0, 1, 0]):
        '''
        метод позволяет исходя из action получить direction движения змейки,
        action при этом предсказывается нейронной сетью
        
        '''
        directions_order = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        current_direction_order = directions_order.index(self.snake.direction)
        new_direction_order = current_direction_order + 0
        if np.array_equal(action, [0, 1, 0]):
            new_direction_order = current_direction_order
        elif np.array_equal(action, [0, 0, 1]):
            new_direction_order = (current_direction_order + 1) % 4
        else:       # если None остается пока agent.get_action() не сделан, то будет влево крутить
            new_direction_order = (current_direction_order - 1) % 4

        self.snake.direction = directions_order[new_direction_order]           

    def new_fruit(self):
        self.frame_number = 0
        self.fruit = Fruit(*self.snake.get_pos())
        self.score += 1

    def mainloop_step(self, action=[0, 1, 0]):
        '''Теперь предсказанный action передается сюда,
        затем он передается в move, а потом исходя из action, 
        смотрится direction и выбирается скорость и змейка смещается

        reward назначается за каждый отдельный ход
        '''
        # print(self.snake.direction)
        # x, y = self.snake.head
        # print(self.will_be_dead((x, y)))

        self.reward = 0
        self.frame_number += 1

        self.clock.tick(FPS)
        self.display.fill((0, 0, 0))
        self.update_drawing()

        old_score = self.score
        self.direction_from_action(action)
        self.snake.move(self.fruit.pos)
        new_score = self.score

        self.is_looped()
        if new_score - old_score > 0:
            self.reward = 5
        elif not self.snake.alive:
            self.reward = -5
        

        self.display.blit(self.screen, (0, BAR_HEIGHT))
        pygame.display.flip()

        for event in pygame.event.get():
            self.frame_number += 1
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            # для теста:
            # if event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_UP:
            #         self.snake_up()
            #     if event.key == pygame.K_DOWN:
            #         self.snake_down()
            #     if event.key == pygame.K_LEFT:
            #         self.snake_left()                        
            #     if event.key == pygame.K_RIGHT:
            #         self.snake_right()

        return self.reward, not self.snake.alive, self.score

# Нельзя оставлять здесь main так как это вызывает circular import

# def main():
#     aigame = AI_Game()
#     agent = Learning_Agent()
#     while True:
#         aigame.mainloop_step([0, 1, 0])
#         #print(aigame.mainloop_step())
#         print(agent.get_state(aigame))

#         if not aigame.snake.alive:
#             print(aigame.score)
#             #aigame.reset()
#             break


# if __name__ == "__main__":
#     pygame.init()
#     main()