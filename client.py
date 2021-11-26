import socket


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # создаем аналогичный сокет, как у сервера
s.connect(("localhost", 10000)) # коннектимся с сервером
# "localhost"

tm = s.recv(1024) # Принимаем не более 1024 байта данных


s.close() # закрываем соединение
print("Текущее время: %s" % tm.decode("utf-8")) # получаем данные, декодировав байты
