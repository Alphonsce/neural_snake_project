import torch
import torch.nn as nn
import numpy as np
import pygame
import random
from collections import deque
import matplotlib.pyplot as plt

from model import *
from constans import *
from for_AI_snake.training_model import *

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

        self.model = Neural_network(11, 256, 3)       # нейронная сеть с 11 входными нейронами(state) и 3 выходными (action)
        self.trainer = Q_func_Trainer(self.model, LR, GAMMA)     # это то, что оптимизирует выбранную функцию потерь, используя нейронную сеть, в которой веса обновляются при помощи Adam алгоритма

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

        if self.model.was_loaded:
            '''если модель была загружена, то ее уже не надо обучать и мы случайность убираем'''
            self.epsilon = 0

        if random.randint(0, 200) < self.epsilon:       # epsilon постепенно уменьшается и случацность постепенно пропадет
            index_of_action = random.randint(0, 2)
            final_action[index_of_action] = 1
        else:
            tensor_state = torch.tensor(state, dtype=torch.float)
            prediction = self.model(tensor_state)   # np.array вида [x y z]
            index_of_action = torch.argmax(prediction).item()       # получаем индекс макс элемента и из torch.tensor и item() переводит его в int
            final_action[index_of_action] = 1
        
        return final_action

class AI_Game:
    def __init__(self):
        self.rule = Snake.standart_rule
        self.clock = pygame.time.Clock()
        self.display = pygame.display.set_mode((WIDTH, HEIGHT))
        # field init:
        self.walls = []
        self.reset()
        self.GAME_RUNNING = True

    def reset(self):
        '''здесь находятся все параметры для инициализации игры заново'''
        self.frame_number = 0
        self.score = 0
        self.snake = Snake(FIELD_SIZE_W // 2, FIELD_SIZE_H // 2, self, mode="learning")
        self.fruit = Fruit(*self.snake.get_pos(), self.walls)
        self.screen = pygame.Surface((WIDTH, HEIGHT - BAR_HEIGHT))

    def update_drawing(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(draw_field_AI(
            self.screen, *self.snake.get_pos(), 
            self.fruit.pos
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
        self.fruit = Fruit(*self.snake.get_pos(), self.walls)
        self.score += 1

    def mainloop_step(self, action=[0, 1, 0]):
        '''Теперь предсказанный action передается сюда,
        затем он передается в move, а потом исходя из action, 
        смотрится direction и выбирается скорость и змейка смещается

        reward назначается за каждый отдельный ход
        '''
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
        pygame.draw.rect(self.display, GRAY, [0, 0, WIDTH, BAR_HEIGHT])
        self.display.blit(self.screen, (0, BAR_HEIGHT))
        pygame.display.flip()
        for event in pygame.event.get():
            self.frame_number += 1
            if event.type == pygame.QUIT:
                self.GAME_RUNNING = False
        return self.reward, not self.snake.alive, self.score

class Graph_plotter:
    def __init__(self, scores, mean_scores) -> None:
        plt.ion()
        plt.figure(1)
        self.draw_graph(scores, mean_scores)
        
    def draw_graph(self, scores, mean_scores):
        '''функция для отрисовки графика обучения
        '''        
        plt.clf()
        plt.text(len(scores) - 1, scores[-1], str(scores[-1]))     # пишет возле графика со scores какой последний score
        plt.text(len(scores) - 1, mean_scores[-1], str(round(mean_scores[-1], 3)))        # пишет mean_score возле графика со средними

        plt.xlabel('Количество игр')
        plt.ylabel('Набранные очки')

        plt.plot(scores, label='Очки')
        plt.plot(mean_scores, label='Среднее')
        plt.legend(loc='upper left', fontsize=10)
        plt.ylim(ymin=0)

        plt.pause(0.1)
    
    def finish(self, scores, mean_scores):
        plt.ioff()
        self.draw_graph(scores, mean_scores)

def training_process():
    '''Функция, которая запускает само обучение нейронной сети,
    '''
    scores = [0]
    mean_scores = [0]
    plotter = Graph_plotter(scores, mean_scores)

    best_score = 0
    agent = Learning_Agent()
    game = AI_Game()
    while game.GAME_RUNNING:
        old_state = agent.get_state(game)

        move = agent.get_action(old_state)

        reward, game_over, score = game.mainloop_step(move)     # 1 сдвиг змейки и получение результатов этого сдвига

        new_state = agent.get_state(game)

        # обучение для 1 итерации:
        agent.short_memory_train(old_state, move, reward, new_state, game_over)
        agent.add_to_memory(old_state, move, reward, new_state, game_over)

        # когда закончилась игра делаем обучение на всей памяти
        if game_over:
            scores = np.append(scores, score)

            game.reset()
            agent.number_of_games += 1

            mean_scores = np.append(mean_scores, np.sum(scores) / agent.number_of_games)
            
            plotter.draw_graph(scores, mean_scores)

            agent.long_memory_train()

            if score > best_score:
                best_score = score
                agent.model.save()
            
            print('game:', agent.number_of_games, 'score:', score)
    plotter.finish(scores, mean_scores)
    
def draw_field_AI(surf, snake_tail, snake_head, fruit):
    """ Функция рисует поле.
    Первоначльно она должна нарисовать темное поле
    Исходя из массива надо нарисовать квадратики в клеточках: 
    surf - Поле на котором надо нарисовать.
    cells - массив чисел. Соответствия устанавливаются с помощью 
    класса Cell в модуле constans
    Фрукт - красный (занимает 80% ширины и высоты клетки)
    Змея - зеленая (занимает 80% ширины и высоты клетки)
    Голова - Зеленая (занимает 100% ширины и высоты клетки)
    Также для каждой части змеи надо сделать соединение между двумя клеточками -
    Салатовая, например(занимает 80% ширины или высоты клетки)
    """
    (x_0, y_0) = fruit
    x_0 *= CELL_SIDE
    y_0 *= CELL_SIDE
    pygame.draw.rect(surf, RED, (x_0, y_0, CELL_SIDE, CELL_SIDE))
    k = 0.5 * (1 - WIDTH_OF_TAIL)
    (x_0, y_0) = snake_head
    (x, y) = snake_tail[-1]
    pygame.draw.rect(surf, BLUE, (int(x_0 * CELL_SIDE), int(y_0 * CELL_SIDE), CELL_SIDE, CELL_SIDE))
    for i in range(len(snake_tail)):
        (x, y) = snake_tail[-i - 1]
        pygame.draw.rect(surf, BLUE, (
            int((min(x, x_0) + k) * CELL_SIDE),
            int((min(y, y_0) + k) * CELL_SIDE),
            int(CELL_SIDE * (1 + abs(x - x_0) - 2 * k)),
            int(CELL_SIDE * (1 + abs(y - y_0) - 2 * k))
            ))
        (x_0, y_0) = (x, y)
    return surf

