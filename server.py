import socket
from settings import Settings
import threading
import datetime
import os
import image_to_html

settings = Settings()  # Создаём переменную в которой хранятся настройки

sock = socket.socket()

# Подключаемся и начинаем прослушивать порт, указанный в настройках
try:
    sock.bind(('', settings.port))
    print(f"Using port {settings.port}")
except OSError:
    sock.bind(('', settings.port2))
    print(f"Using port {settings.port2}")
sock.listen(5)

conn, addr = sock.accept()
print("Connected", addr, "\n")

directory = settings.directory

# Получение инфы от клиента
data = conn.recv(settings.request_size)
msg = data.decode()
print(msg)

# Получаем имя файла, который отправим клиенту
name = msg.split()[1][1:]

if name == "":
    name = "index.html"
name = directory + "\\" + name

# Вычисление текущего времени и приведение его к необходимому формату
now = datetime.datetime.now()
date = now.strftime("%a, %d %b %Y %H:%M:%S GTM")

# Вывод в лог файл основной инфы
with open("log.txt", "a") as log:
    print(f"Date: {date}\nAddr: {addr}\nFile: {name}", file=log)

# Формирование ответа на запрос
try:
    size = os.path.getsize(name)  # Размер ответа

# Если файла с таким именем нет
except FileNotFoundError:
    resp = f"""HTTP/1.1 404 OK
    Server:SelfMadeServer v0.0.1
    Date: {date}
    Connection: keep-alive
    """
    with open("log.txt", "a") as log:
        print("Error: 404", file=log)

    resp = resp.encode()
else:
    decr = name.split(".")[-1]  # Получение расширения
    if decr not in settings.types:
        resp = f"""HTTP/1.1 403 OK
        Server:SelfMadeServer v0.0.1
        Date: {date}
        Connection: keep-alive
        """
        with open("log.txt", "a") as log:
            print("Error: 403", file=log)
    try:
        # Если файл текстовый
        with open(name, "r", encoding="utf-8") as file:
            resp = f"""HTTP/1.1 200 OK
            Server: SelfMadeServer v0.0.1
            Date: {date}
            Content-Type: text/html;charset=utf-8
            Content-Length: {size}
            Connection: keep-alive

            """
            resp += file.read()
        resp = resp.encode()
        # Если файл бинарный
    except UnicodeDecodeError:
        # Если файл картинка
        if decr in settings.pictures:
            resp = f"""HTTP/1.1 200 OK
            Server: SelfMadeServer v0.0.1
            Date: {date}
            Content-Type: text/image/html;charset=utf-8
            Content-Length: {size}
            Connection: keep-alive

            """
            resp += image_to_html.magic(name)
            resp = resp.encode()
        else:
            resp = f"""HTTP/1.1 200 OK
            Server: SelfMadeServer v0.0.1
            Date: {date}
            Content-Type: bytes
            Content-Length: {size}
            Connection: keep-alive
    
            """
            resp = resp.encode()
            with open(name, "rb") as file:
                resp += file.read()

conn.send(resp)

conn.close()
