import random
import socket
import time
import json

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

    def update(self, direction=None):
        if direction != None:
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
            x, y = (random.randint(FIELD_SIZE_W + 3, self.game.field_size - FIELD_SIZE_W - 4),
                random.randint(FIELD_SIZE_H + 3, self.game.field_size - FIELD_SIZE_H - 4))
            not_found = False 
            for i in range(-3, 4, 1):
                for j in range(-3, 4, 1):
                    if self.game.cell[x + i][y + j].value != 0:
                        not_found = True
        self.snake = SnakeVS(x, y, self.game, self)

class Server:
    def __init__(self, Num_of_players) -> None:
        self.Num_of_pl = Num_of_players
        self.broad = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.broad.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.message = "Wellcome snake online".encode('utf-8') 
        self.broad.settimeout(0.02)

        self.serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serv.bind(("", 11001))
        self.serv.listen(Num_of_players) 
        self.serv.settimeout(0.02)
        self.connected = False

        self.gamers = []
        self.field_size_w = FIELD_SIZE_W * 2 + 10 * Num_of_players + 10
        self.field_size_h = FIELD_SIZE_H * 2 + 10 * Num_of_players + 10
        self.cell = [[Cell.Nothing]*self.field_size_h]*self.field_size_w
        self.fruits =[]
        for i in range((Num_of_players+1)//2):
            self.fruits.append(FruitVS(self))
        self.walls = [*((FIELD_SIZE_W - 1, y) for y in range(self.field_size_h)),
            *((self.field_size_w - FIELD_SIZE_W, y) for y in range(self.field_size_h))
            *((x, FIELD_SIZE_H - 1) for x in range(self.field_size_w)),
            *((x, self.field_size_h - FIELD_SIZE_H) for x in range(self.field_size_w))
        ]

    def join(self):
        try:
            data, addr = self.broad.recvfrom(1024)
        except:
            data = ""
        if data == b"Hello Snake11002":
            client, addr = self.serv.accept()
            self.gamers.append(Gamer(client, addr, self))

    def broadcast(self):
        self.broad.sendto(self.message, ('<broadcast>', 11002))
        print("message sent!")
        if len(self.gamers) == self.Num_of_pl:
            self.broad.close()
            self.connected = True

    def update(self):
        if self.connected:
            for item in self.gamers:
                direction = Direction.RIGHT # FIXME
                item.update(direction)
                try:
                    item.client.send(json.dumps([1, 2, 3]).encode('utf-8'))
                except:
                    pass

            self.cell = [[Cell.Nothing]*self.field_size]*self.field_size
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
                self.cell[x][y] = Cell.Wall


            for i in range(10):
                try:
                    self.serv.recvfrom(1024)
                except:
                    pass
        

    def stop(self):
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

