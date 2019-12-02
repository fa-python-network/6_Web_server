import socket
from settings import Settings
import threading
import datetime
import os


def create_status(addr, data, dir, dict):
    """Создание статусной строки"""
    file = data.split()[1][1:]  # Имя файла
    if file == "": file = "index.html"
    rasch = file.split(".")[-1]  # Расширение
    files = os.listdir(dir)  # Список всех файлов в директории сервера

    code = "200 OK"
    con = "keep-alive"
    if rasch not in dict.keys():
        code = "403 Forbidden"
        con = "close"
    if file not in files:
        code = "404 Not Found"
        con = "close"

    file = dir + "\\" + file  # Путь к файлу
    date = datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S GTM")  # Время
    # Запись в лог файл
    with open("log.txt", "a") as log:
        print(f"Date: {date}\nAddr: {addr}\nFile: {file}", file=log)
        if code != "200 OK":
            print(f"Error: {code}", file=log)
        print("", file=log)

    # Формирование статусной строки
    status = f"""HTTP/1.1 {code}
Server:SelfMadeServer v0.0.1
Date: {date}
Connection: {con}"""

    if code != "200 OK":
        return status.encode(), 0, file

    size = os.path.getsize(file)
    cont = dict[rasch]
    status += f"""
Content-Type: {cont}
Content-Length: {size}

"""

    return status.encode(), 1, file


def create_main_request(file):
    try:
        with open(file, "r", encoding="utf-8") as file:
            resp = file.read()
        return resp.encode()
    except UnicodeDecodeError:
        with open(file, "rb") as file:
            resp = file.read()
        return resp


def connection(conn, addr, dir, size, dict):
    data = conn.recv(size)
    if not data:
        return
    data = data.decode()
    print(data)

    request, flag, file = create_status(addr, data, dir, dict)
    if not flag:
        conn.send(request)
        print(request)
        conn.close()
        return
    request += create_main_request(file)
    conn.send(request)
    print(request)


sett = Settings()
sock = socket.socket()

try:
    sock.bind(('', sett.port))
    print(f"Using port {sett.port}")
except OSError:
    sock.bind(('', sett.port2))
    print(f"Using port {sett.port2}")
sock.listen(5)

while True:
    conn, addr = sock.accept()
    print("Connected", addr, "\n")
    tr = threading.Thread(target=connection, args=(conn, addr, sett.directory, sett.request_size, sett.dict))
    tr.start()
