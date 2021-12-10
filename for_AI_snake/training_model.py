import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import os

class Neural_network(nn.Module):
    '''просто сама нейронная сеть'''
    def __init__(self, input_size, hidden_size, output_size):
        self.was_loaded = False
        super().__init__()
        self.linear1 = nn.Linear(input_size, hidden_size)
        self.linear2 = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        x = x       # входной слой
        x = F.relu(self.linear1(x))     # скрытый слой с функцией активации
        x = self.linear2(x)     # просто линейные комбинации весов со значениями в нейронах на предыдущем слое - выходной слой без функции активации

        return x

    def save(self, file_name='model.pth'):
        model_folder_path = './model'
        if not os.path.exists(model_folder_path):
            os.makedirs(model_folder_path)

        file_name = os.path.join(model_folder_path, file_name)
        torch.save(self.state_dict(), file_name)

    def load(self, path='./model/learned_model.pth'):
        self.load_state_dict(torch.load(path))
        self.was_loaded = True


class Q_func_Trainer:
    '''то что обновляет коэффициенты нейронной сети'''
    def __init__(self, model, lr, gamma):
        self.lr = lr
        self.gamma = gamma
        self.model = model
        self.optimizer = optim.Adam(model.parameters(), lr=self.lr)     # по-сути это градиентный спуск, только более опимизированный
        self.criterion = nn.MSELoss()       # функция ошибки - среднее значение квадрата отклонения

    def train_step(self, state, action, reward, next_state, game_over):
        state = torch.tensor(state, dtype=torch.float)
        next_state = torch.tensor(next_state, dtype=torch.float)
        action = torch.tensor(action, dtype=torch.long)
        reward = torch.tensor(reward, dtype=torch.float)

        if len(state.shape) == 1:       # обучение на 1 итерации

            state = torch.unsqueeze(state, 0)
            next_state = torch.unsqueeze(next_state, 0)
            action = torch.unsqueeze(action, 0)
            reward = torch.unsqueeze(reward, 0)
            game_over = (game_over, )

        prediction = self.model(state)      # model(state) выполняет model.forward, вот так вот torch работает, в итоге имеем Q для 3 выходных нейронов

        target = prediction.clone()
        for idx in range(len(game_over)):
            # на всём batch'е обучаемся
            Q_new = reward[idx]     # если игра еще не закончилась, то мы большого прогона не делаем и полагаем что максимальный выход - reward в ход после предсказания
            
            if not game_over[idx]:
                Q_new = reward[idx] + self.gamma * torch.max(self.model(next_state[idx]))       # уравнение Беллмана, оно использует как раз reward 
# В уравнении Беллмана мы находим потенциально максимальный выход нейронной сети в следующий ход после того хода, для которого уже предсказали выход
            target[idx][torch.argmax(action[idx]).item()] = Q_new
    
        self.optimizer.zero_grad()

        loss = self.criterion(target, prediction)       # функция потерь - это MSE между Q в текущем положении и максимальным Q в следующем положении

# Допустим нейронная сеть выдала нам прогнозы вида: [5, 2, 1] - отсюда мы должны выполнить действие [1, 0, 0], но значения Q соответственно равны 5, 2, 1
# затем используя уравнение Беллмана мы находим максимально возможное значение Q функции для следующего действия, пусть оно равно [10, 7, 5]
# тогда loss у нас получится (25 + 9 + 16) / 3

        loss.backward()     # это просто последний этап back propagation

        self.optimizer.step()
