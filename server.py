import socket
from settings import Settings
import threading
import datetime
import os


# Функция обрабатывающая запрос
def request(conn, addr, data, directory):
    # Получение инфы от клиента
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
        resp = f"""HTTP/1.1 404 Not Found
        Server:SelfMadeServer v0.0.1
        Date: {date}
        Connection: keep-alive
        """
        with open("log.txt", "a") as log:
            print("Error: 404", file=log)

        resp = resp.encode()
    else:
        decr = name.split(".")[-1]  # Получение расширения
        if decr not in settings.dict.keys():
            resp = f"""HTTP/1.1 403 Forbidden
            Server:SelfMadeServer v0.0.1
            Date: {date}
            Connection: keep-alive
            """
            with open("log.txt", "a") as log:
                print("Error: 403", file=log)
        else:
            try:
                # Если файл текстовый
                with open(name, "r", encoding="utf-8") as file:
                    resp = f"""HTTP/1.1 200 OK
                    Server: SelfMadeServer v0.0.1
                    Date: {date}
                    Content-Type: text/{decr};charset=utf-8
                    Content-Length: {size}
                    Connection: keep-alive

                    """
                    resp += file.read()
                resp = resp.encode()
                # Если файл бинарный (картинка)
            except UnicodeDecodeError:
                resp = f"""HTTP/1.1 200 OK
                Server: SelfMadeServer v0.0.1
                Date: {date}
                Content-Type: image/{decr}
                Content-Length: {size}
                Connection: keep-alive

                """
                resp = resp.encode()
                with open(name, "rb") as file:
                    resp += file.read()
    conn.send(resp)
    print(resp)


# Функция для работы с клиентами
def connection(conn, addr, directory):
    data = conn.recv(settings.request_size)
    if not data:
        return
    request(conn, addr, data, directory)
    conn.close()


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

directory = settings.directory

# На каждое подключение - свой поток
conn, addr = sock.accept()
while True:
    print("Connected", addr, "\n")
    tr = threading.Thread(target=connection, args=(conn, addr, directory))
    tr.start()
    conn, addr = sock.accept()