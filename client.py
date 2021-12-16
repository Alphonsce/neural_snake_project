import json
import socket

from constans import *

"""s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # создаем аналогичный сокет, как у сервера
s.connect(("localhost", 10000)) # коннектимся с сервером
# "localhost"

tm = s.recv(1024) # Принимаем не более 1024 байта данных


s.close() # закрываем соединение
print("Текущее время: %s" % tm.decode("utf-8")) # получаем данные, декодировав байты"""


class Client:
    """Клиент для игры по сети"""
    def __init__(self, gameVS) -> None:
        """Инициализация клиента в виде двух сокетов для 
        основной передачи данных и принятия/отправки дополнительных сообщений"""
        self.game = gameVS
        self.serv = None
        self.gs2 = False

        self.broadcaster = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.broadcaster.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.broadcaster.bind(("", 11002))
        self.message = "Hello Snake11002".encode('utf-8') 
        self.broadcaster.settimeout(0.002)

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.walls = []
        self.snakes = []
        self.fruits = []
        self.connected = False
        self.game_started = False
        self.socket.settimeout(0.002)
        #self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)


    def check_server_fall(self):
        """ Проверка на наличие подключения к серверу."""

        return self.connected

    def send_direction(self, direction):
        """ Отправка информации о нажатых игроком кнопках"""
        try:
            self.socket.send((json.dumps(direction.value)).encode('utf-8'))
        except:
            pass

    def get_information(self):
        """ Обновление информации об игровом поле"""
        try:
            s = self.socket.recv(32000).decode('utf-8')
            if self.gs2:
                self.snakes, self.fruits = tuple(json.loads(s))

            else:
                self.walls = json.loads(s)
                self.gs2 = True
        except:
            pass


    def update(self):
        """ Шаг цикла клиента"""
        self.look_up_server()
        if self.game_started:
            self.get_information()
            self.send_direction(self.game.snake)
        

    def look_up_server(self):
        """ Проверка наличия сообщений от Сервера"""
        try:
            data, (addr, port) = self.broadcaster.recvfrom(1024)
        except:
            data = b""
        data = data.decode('utf-8')
        if data != "":
            print(data)
        if data == "Wellcome snake online" and not self.connected:
            self.serv = (addr, port)
            self.broadcaster.sendto(self.message, (addr, port))
            self.socket.settimeout(2)
            self.socket.connect((addr, 11001))
            self.socket.settimeout(0.002)
            print("connected")
            self.connected = True
        elif data == "Start game" and self.connected:
            print("game started")
            self.game_started = True
        elif data == "Stop game" and self.connected:
            self.game.stop_client()
            self.connected = False

    def stop(self):
        """ Остановка подключения """
        #self.broadcaster.close()
        self.socket.close()

    def quit_game(self):
        """ Выход из игры с отправкой сообщения на сервер"""
        if self.serv != None:
            self.broadcaster.sendto(b"GoodBuy Snake11002", self.serv)


"""import time
x= 0
cl = Client(2)
while x < 30:
    x +=1 
    time.sleep(1)
    cl.update()
    print(x)"""
