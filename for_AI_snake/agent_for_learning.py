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
        self.epsilon = 0

        self.model = training_model.Neural_network(11, 256, 3)       # нейронная сеть с 11 входными нейронами(state) и 3 выходными (action)
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
        # аппендим один tuple из характеристик на текущем шагу в память
        self.memory.append((state, action, reward, next_state, game_over))    # memory - это deque с удалением левого края, когда переполнено

    def long_memory_train(self):
        '''обучается на всей памяти(ее части размером в batch), которую мы создаем при помощи add_to_memory'''
        if len(self.memory) > BATCH_SIZE:
            part_of_memory = random.sample(self.memory, BATCH_SIZE)     # возвращает список tuple'ов, если в памяти больше чем выбранный batch, то берем случайные элементы из памяти
        else:
            part_of_memory = self.memory

        states, actions, rewards, next_states, game_overs = zip(*part_of_memory)
        self.trainer.train_step(states, actions, rewards, next_states, game_overs)

    def short_memory_train(self, state, action, reward, next_state, game_over):
        '''обучение на 1 итерации цикла'''
        self.trainer.train_step(state, action, reward, next_state, game_over)

    def get_action(self, state):
        #return [0, 1, 0] если хочется сделать проверку.
        # действия в начале будет случайными, затем с количеством эпох, случайность будет снижаться
        final_action = [0, 0, 0]
        self.epsilon = STARTING_EPSILON - self.number_of_games
        if random.randint(0, 200) < self.epsilon:       # epsilon постепенно уменьшается и случацность постепенно пропадет
            index_of_action = random.randint(0, 2)
            final_action[index_of_action] = 1
        else:
            tensor_state = torch.tensor(state, dtype=torch.float16)
            prediction = self.model.predict(tensor_state)   # np.array вида [x y z]
            index_of_action = torch.argmax(prediction).item()       # получаем индекс макс элемента и из torch.tensor и item() переводит его в int
            final_action[index_of_action] = 1
        
        return final_action



# Можно потом перенести эту функцию в AI_snake и оттуда инициализировать начало обучения
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
            
            print('game:', agent.number_of_games, 'score:', score)

if __name__ == '__main__':
    training_process()