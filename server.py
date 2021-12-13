import random
import socket
import time
import json
import pygame
from numpy import sqrt

from constans import *
from modelVS import *


"""serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Создается сокет протокола TCP
serv.bind(("", 10000)) # Присваиваем ему порт 10000
serv.listen(1) # Максимальное количество одновременных запросов
# broadcast
t = time.time()
while t + 60 > time.time():
    client, addr = serv.accept() # акцептим запрос на соединение
    print(client)
    print("Запрос на соединение от %s" % str(addr))
    timestr = time.ctime(time.time()) + "\n"
    client.send(timestr.encode("utf-8")) #передаем данные, предварительно упаковав их в байты
    client.close() # закрываем соединение


serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv.bind(("", 11002))
serv.listen(10) """

class Gamer:
    def __init__(self, client, addr, game) -> None:
        self.client = client
        self.addr = addr
        self.game = game
        self.new_snake()
        self.score = 0
        self.current_score = 0
        self.deaths = 0

    def update(self, direction):
        self.snake.direction = direction
        self.snake.move()

    def death(self):
        self.deaths += 1
        self.score += self.current_score
        self.current_score = 0
        self.new_snake()

    def new_snake(self):
        not_found = True
        while not_found:
            x, y = (random.randint(FIELD_SIZE_W + 3, self.game.field_size_w - FIELD_SIZE_W - 4),
                random.randint(FIELD_SIZE_H + 3, self.game.field_size_h - FIELD_SIZE_H - 4))
            not_found = False 
            for i in range(-3, 4, 1):
                for j in range(-3, 4, 1):
                    if self.game.cell[x + i][y + j].value != 0:
                        not_found = True
            #print(x, y)
        self.snake = SnakeVS(x, y, self.game, self)

class Server_Game:
    def __init__(self, Num_of_players, gamers) -> None:
        self.gamers = gamers

        self.field_size_w = FIELD_SIZE_W * 2 + int(20 * sqrt(Num_of_players))
        self.field_size_h = FIELD_SIZE_H * 2 + int(20 * sqrt(Num_of_players))

        self.cell = [0]*self.field_size_w
        for i in range(self.field_size_w):
            self.cell[i]=[Cell.Nothing]*self.field_size_h

        self.fruits =[]
        for i in range((Num_of_players+1)//2):
            self.fruits.append(FruitVS(self))

        self.walls = [*((FIELD_SIZE_W - 1, y) for y in range(self.field_size_h)),
            *((self.field_size_w - FIELD_SIZE_W, y) for y in range(self.field_size_h)),
            *((x, FIELD_SIZE_H - 1) for x in range(self.field_size_w)),
            *((x, self.field_size_h - FIELD_SIZE_H) for x in range(self.field_size_w))
        ]

    def update(self):
        self.cell = [0]*self.field_size_w
        for i in range(self.field_size_w):
            self.cell[i]=[Cell.Nothing]*self.field_size_h
        for gamer in self.gamers:
            x, y = gamer.snake.head
            self.cell[x][y] = Cell.Head
            for item in gamer.snake.tail:
                x, y = item
                self.cell[x][y] = Cell.Snake
        for item in self.fruits:
            x, y = item.pos
            self.cell[x][y] = Cell.Fruit
        for item in self.walls:
            x, y = item
            self.cell[x][y] = Cell.Snake


class Server:
    def __init__(self, Num_of_players) -> None:
        self.Num_of_pl = Num_of_players
        self.broad = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.broad.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.message = "Wellcome snake online".encode('utf-8') 
        self.broad.settimeout(0.002)

        self.serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serv.bind(("", 11001))
        self.serv.listen(Num_of_players) 
        self.serv.settimeout(0.002)
        self.connected = False

        self.gamers = []
        self.game = Server_Game(Num_of_players, self.gamers)
        self.last_broadcast = pygame.time.get_ticks()
        

    def join(self):
        try:
            data, addr = self.broad.recvfrom(1024)
        except:
            data = ""
        if data == b"Hello Snake11002":
            
            self.serv.settimeout(2)
            client, addr = self.serv.accept()
            self.gamers.append(Gamer(client, addr, self.game))
            self.serv.settimeout(0.002)
            print(len(self.gamers))
            if len(self.gamers) == self.Num_of_pl:
                self.connected = True
                self.broad.sendto("Start game".encode('utf-8'), ('<broadcast>', 11002))
                print("game started")
                for item in self.gamers:
                    data = self.game.walls
                    item.client.send(json.dumps(data).encode('utf-8'))

    def broadcast(self):
        self.broad.sendto(self.message, ('<broadcast>', 11002))
        print("message sent!")
                  
    def check_quits(self):
        try:
            data, addr = self.broad.recvfrom(1024)
        except:
            data = ""
        if data == b"GoodBuy Snake11002":
            self.stop()
        return not (data == b"GoodBuy Snake11002")

    def update(self):
        if self.connected:
            print(self.gamers)
            if self.check_quits():
                data = [
                    [[gamer.snake.step, gamer.snake.head, gamer.snake.tail] for gamer in self.gamers],
                    [fruit.pos for fruit in self.game.fruits]
                    ]
                
                for item in self.gamers:
                    for i in range(self.Num_of_pl):
                        if item is self.gamers[i] and i != 0:
                            c = data[0][0].copy()
                            data[0][0] = data[0][i].copy()
                            data[0][i] = c
                            #data[0][i], data[0][0] = data[0][0] , data[0][i]"""
                    try:
                        item.client.send(json.dumps(data).encode('utf-8'))
                    except:
                        self.stop()
                    print("waiting")
                    try:
                        data_client = item.client.recv(1024)
                        direction = Direction(tuple(json.loads(data_client.decode('utf-8'))))
                    except:
                        direction = Direction(item.snake.speed)
                    item.update(direction)
                self.game.update()
            
        else:
            now = pygame.time.get_ticks()
            if now - self.last_broadcast > 1000:
                self.broadcast()
                self.last_broadcast = now
            self.join()

    def stop(self):
        self.broad.sendto("Stop game".encode('utf-8'), ('<broadcast>', 11002))
        #self.broad.close()
        self.serv.close()

"""from client import *
player1 = Client()
serv = Server(5)
x = 1
while x < 20: 
    x += 1
    time.sleep(1)
    serv.broadcast()
    serv.join()
    serv.update()
    if 5 < x < 10:
        player1.update()"""

"""
player = Client()
x = 1
while x < 60: 
    x += 1
    time.sleep(1)
    player.update()

"""
"""
from client import *
player1 = Client()
serv = Server(5)
x = 1
while x < 30: 
    x += 1
    time.sleep(1)
    if x % 3 == 0:
        serv.broadcast()
    serv.join()
    serv.update()
    player1.update()"""

""" data = [
                [[gamer.snake.step, gamer.snake.head, gamer.snake.tail] for gamer in self.gamers],
                [fruit.pos for fruit in self.game.fruits]
                ]
            for item in self.gamers:
                try:
                    for i in self.Num_of_pl:
                        if item is self.gamers[i]:
                            data[0][i], data[0][0] = data[0][0] , data[0][i]"""