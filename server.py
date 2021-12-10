import socket
import time
import json

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

    def update(self):
        self.snake.move()

    def death(self):
        self.deaths += 1
        self.score += self.current_score
        self.current_score = 0
        self.new_snake()

    def new_snake(self):
        pass

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
        self.gamers = []

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

    def update(self):
        for item in self.gamers:
            item.client.send(json.dumps([1, 2, 3]).encode('utf-8'))

    def stop(self):
        self.serv.close()

from client import *
player1 = Client()
serv = Server(5)
x = 1
while x < 60: 
    x += 1
    time.sleep(1)
    serv.broadcast()
    serv.join()
    serv.update()
    player1.update()

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

