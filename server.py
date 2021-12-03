import socket
import time

serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Создается сокет протокола TCP
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
serv.listen(10) 

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
        self.serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serv.bind(("", 11002))
        self.serv.listen(Num_of_players) 
        self.gamers = []

    

    def join(self):
        client, addr = serv.accept()
        self.gamers.append(Gamer(client, addr, self))

    def update(self):
        pass



