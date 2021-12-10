import socket


"""s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # создаем аналогичный сокет, как у сервера
s.connect(("localhost", 10000)) # коннектимся с сервером
# "localhost"

tm = s.recv(1024) # Принимаем не более 1024 байта данных


s.close() # закрываем соединение
print("Текущее время: %s" % tm.decode("utf-8")) # получаем данные, декодировав байты"""


class Client:
    def __init__(self) -> None:
        self.broadcaster = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.broadcaster.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.broadcaster.bind(("", 11002))
        self.message = "Hello Snake11002".encode('utf-8') 
        self.broadcaster.settimeout(0.02)

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.walls = []
        self.snakes = []
        self.fruit = []
        self.connected = False
        self.socket.settimeout(0.02)
        #self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)


    def check_server_fall(self):
        pass

    def send_direction(self, direction):
        pass

    def get_information(self):
        try:
            text = self.socket.recv(1024)
            print(text.decode('utf-8'))
        except:
            pass

    def update(self):
        if self.connected:
            self.get_information()
        else:
            self.look_up_server()

    def look_up_server(self):
        try:
            data, (addr, port) = self.broadcaster.recvfrom(1024)
        except:
            data = ""
        if data == b"Wellcome snake online" and not self.connected:
            self.broadcaster.sendto(self.message, (addr, port))
            self.socket.connect((addr, 11001))
            print(data.decode('utf-8'))
            self.connected = True

    def stop(self):
        self.socket.close()

