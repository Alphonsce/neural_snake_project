import torch
import torch.nn as nn
import numpy as np
import random
from collections import deque
from AI_snake import AI_Game, Direction
from AI_constans import MAX_MEMORY
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

        self.model = None       # нейронная сеть с 11 входными нейронами(state) и 3 выходными (action)
        self.trainer = None     # это сам "обучатель" - алгоритм, который обучает нейронную сеть self.model, минимизируя Q функцию принятия решения


    def get_state(self, game_class=AI_Game()):
        '''метод получения state
        '''
        pass

    def add_to_memory(self):
        pass

    def long_memory_train(self):
        pass

    def short_memory_train(self):
        pass

    def get_action(self, state):
        pass



def training_process():
    '''Функция, которая запускает само обучение нейронной сети,
    '''
    pass