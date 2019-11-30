import socket
import re
import json
import logging
import os
import threading
import datetime
from time import sleep

def openfi(filename, type='rb'): # Открытие файлов.
    with open(filename, type) as file:
                return file.read()


with open('config.json') as file:
    config = json.load(file)
MAX = config['MAX'] # Максимум бит в одном запросе
PORT = config['PORT'] # Порт
DIR = config['DIR'] # Рабочая директория
LIS = config['LIS'] # Кол-во прослушиваемых
ADRESS = config['ADR']
os.chdir(DIR)
logging.basicConfig(filename="log_serv", level=logging.INFO) # Логирование

head = ['HTTP/1.1 200 OK', 'Server: Pokekek 0.02', 'Content-type: text/html', 'Connection: close', '', ''] # Список редактируемый в процессе.
PAT = re.compile(r'[A-Z]{3,6}\s[\S]*\sHTTP/[0-9.]*', flags=re.MULTILINE) #  Создание паттерна
htmllist = ['index.html', 'favicon.ico']





class Response: #  Класс овтета, формируется на основе запроса.
    def __init__(self, html ):
        self.head = head
        logging.info(f'Запрос: {html}')
        if html[1:] in htmllist: #  Базовая операция доставания файла.
            if 'favicon.ico' in html:
                self.head[2] = 'Content-type: image/ico'
            self.html = openfi(html[1:])
        elif html == '/': #  Страница по умолчанию.
            self.html = openfi('index.html')
        else:  #  Ветка ошибки.
            self.html = openfi('322.html')
            self.head[0] = 'HTTP/1.1 404 Not Found'
        logging.info(self.head[0])
        logging.info(' ')
        print(self.head)
        

    
    def resp(self):
        self.head = '\n'.join(self.head)
        return self.head.encode('UTF-8') + self.html


def parse(req):
    return PAT.findall(req)[0].split(' ')[1] #  Функция обработки запроса с помощью паттерна


def answer(msg, conn):
    html = parse(msg)
    Ans = Response(html)
    conn.send(Ans.resp())
    conn.close()


sock = socket.socket()


try:
    sock.bind((ADRESS, PORT))
    print("Using port 8080")
except OSError:
    sock.bind((ADRESS, 80))
    print("Using port 80")

sock.listen(LIS)
while True:
    conn, addr = sock.accept()
    now = datetime.datetime.now()
    logging.info(now)
    logging.info(f"Connected {addr}")
    sleep(0.01)
    data = conn.recv(MAX)
    msg = data.decode()
    print(msg)
    if msg:
        work = threading.Thread(target=answer, args=[msg, conn])
        work.start()
