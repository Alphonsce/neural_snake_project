import torch
import torch.nn as nn
import numpy as np
import random
from collections import deque

from AI_snake import AI_Game
from AI_constans import *
import training_model


class Learning_Agent:
    '''Агент - это то, что управляет игрой, 
    здесь будет определяться текущее состояние игрового поля: state, 
    затем будет происходить возвращение итогового action исходя из state

    model  и trainer будут реализованы в файле training_model
    '''
    def __init__(self):
        self.number_of_games = 0
        self.memory = deque(maxlen=MAX_MEMORY)      # при переполнении памяти, будет удалять данные из левого края списка
        self.epsilon = EPSILON

        self.model = None       # нейронная сеть с 11 входными нейронами(state) и 3 выходными (action)
        self.trainer = None     # это сам "обучатель" - алгоритм, который обучает нейронную сеть self.model, минимизируя Q функцию принятия решения


    def get_state(self, game_class):
        '''метод получения state

        state - это текущее состояние "среды" агента, в данном случае его полностью
        можно характеризовать 11 булевыми значениями: есть опасность спереди/слева/справа; направление
        движения змейки вперед/назад/влево/вправо; фрукт спереди/сзади/слева/справа
        '''    
        head_x, head_y = game_class.snake.head
        fruit_x, fruit_y = game_class.fruit.pos

        right_point = (head_x + 1, head_y)
        left_point = (head_x - 1, head_y)
        down_point = (head_x, head_y + 1)
        up_point = (head_x, head_y - 1)

        moving_left = (game_class.snake.direction == Direction.LEFT)
        moving_right = (game_class.snake.direction == Direction.RIGHT)
        moving_up = game_class.snake.direction == Direction.UP
        moving_down = game_class.snake.direction == Direction.DOWN

        danger_left = ((moving_down and game_class.will_be_dead(right_point)) or 
            (moving_up and game_class.will_be_dead(left_point)) or
            (moving_right and game_class.will_be_dead(up_point)) or
            (moving_left and game_class.will_be_dead(down_point)))

        danger_straight = ((moving_right and game_class.will_be_dead(right_point)) or 
            (moving_left and game_class.will_be_dead(left_point)) or 
            (moving_up and game_class.will_be_dead(up_point)) or 
            (moving_down and game_class.will_be_dead(down_point)))

        danger_right = ((moving_up and game_class.will_be_dead(right_point)) or 
            (moving_down and game_class.will_be_dead(left_point)) or 
            (moving_left and game_class.will_be_dead(up_point)) or 
            (moving_right and game_class.will_be_dead(down_point)))

        food_left = fruit_x < head_x
        food_right = fruit_x > head_x
        food_up = fruit_y < head_y
        food_down = fruit_y > head_y

        state = [
            danger_left,
            danger_straight,
            danger_right,

            moving_left,
            moving_right,
            moving_up,
            moving_down,

            food_left,
            food_right,
            food_up,
            food_down
        ]
        return np.array(state, dtype=int)

    def add_to_memory(self, state, action, reward, next_state, game_over):
        pass

    def long_memory_train(self):
        # обучается на всей памяти, которую мы создаем при помощи add_to_memory
        pass

    def short_memory_train(self, state, action, reward, next_state, game_over):
        # обучение на 1 итерации цикла
        pass

    def get_action(self, state):
        #return [0, 1, 0] если хочется сделать проверку.
        pass



def training_process():
    '''Функция, которая запускает само обучение нейронной сети,
    '''
    scores = []
    avg_scores = []
    total_score = 0
    best_score = 0
    agent = Learning_Agent()
    game = AI_Game()
    while True:
        old_state = agent.get_state(game)

        move = agent.get_action(old_state)
        #move = [0, 1, 0]

        reward, game_over, score = game.mainloop_step(move)     # 1 сдвиг змейки и получение результатов этого сдвига

        new_state = agent.get_state(game)

        # обучение для 1 итерации:
        agent.short_memory_train(old_state, move, reward, new_state, game_over)
        agent.add_to_memory(old_state, move, reward, new_state, game_over)

        # когда закончилась игра делаем обучение на всей памяти
        if game_over:
            game.reset()
            agent.number_of_games += 1
            agent.long_memory_train()

            if score > best_score:
                best_score = score
                # agent.model.save()
            
            print('game:', agent.number_of_games, 'score:', score, )

if __name__ == '__main__':
    training_process()