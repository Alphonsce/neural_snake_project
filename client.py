import socket


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # создаем аналогичный сокет, как у сервера
s.connect(("localhost", 10000)) # коннектимся с сервером
# "localhost"

tm = s.recv(1024) # Принимаем не более 1024 байта данных


s.close() # закрываем соединение
print("Текущее время: %s" % tm.decode("utf-8")) # получаем данные, декодировав байты


class Client:
    def __init__(self) -> None:
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.walls = []
        self.snakes = []
        self.fruit = []
        pass

    def check_server_fall(self):
        pass

    def send_direction(self, direction):
        pass

    def get_information(self):
        pass

    def look_up_server(self):
        self.socket.connect(("localhost", 11002))

    def stop(self):
        self.socket.close()
