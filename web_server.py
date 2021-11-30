import datetime as c_data
import os
from contextlib import closing
import socket
import threading

class Web_server(threading.Thread):
    def __init__(self, conn, addr, direct):
        super().__init__(daemon=True)
        self.conn = conn
        self.addr = addr
        self.ip = str(addr)
        self.connection()
        self.direct = direct
        self.client_handeling()

    def connection(self):
        print(f'Connection came from: {self.addr}')

    def client_handeling(self):
        while True:
            try:
                fl = self.conn.makefile('r')
            except ConnectionAbortedError:
                break
            msg = fl.readline(customs[2]).split()[1]
            if msg == '/':
                msg = '/index.html'
                file_type = 'html'
            else:
                try:
                    file_type = msg.split('.')[-1]
                except IndexError:
                    file_type = '-'
            fl = os.path.join(self.direct, msg[1:])
            if os.path.exists(fl) == True:
                if file_type == 'txt' or file_type == 'html':
                    file_type = 'text/html'
                    self.response(file_reader(fl), msg, file_type, 'non_error')
                else:
                    self.response("Error 403.  The format is not supported", msg, file_type, '403')
            else:
                self.response("Error 404. File not found", msg, file_type, '404')
        self.conn.close()

    def response(self, resp, msg, file_type, err):
        log_date = str(c_data.datetime.date(c_data.datetime.today()))
        logging(msg, err, log_date, self.ip)
        ln_res = len(resp)
        resp = f"""HTTP/1.1 200 OK
Server: simple_http_server v0.0.1
Content-type: {file_type}
Date: {date}
Connection: close
Date: {date}
Content-length: {ln_res}
{resp}"""
        self.conn.send(resp.encode('utf-8'))

def logging(name, error_code, date, ip):
    f = open(log_name, 'a')
    f.write(date + ' ' + ip + ' ' + name + ' ' + error_code + '\n')
    f.close()

def find_free_port(ip_set):
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind((ip_set, 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]

customs = []
with open('settings.txt', 'r') as f:
    for i in f:
        customs.append(i.split(': ')[1][:-1])
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
customs[0] = int(customs[0])
customs[2] = int(customs[2])
try:

    sock.bind((customs[1], customs[0]))
    print(f"Ваш адрес {customs[1]} {customs[0]}")

except OSError:

    customs[0] = find_free_port(customs[1])
    print(f'Выбранный вами порт уже занят.\nНовый порт: {customs[1]}{customs[0]}')
    sock.bind(('', customs[0]))
customs[0] = str(customs[0])
log_name = 'log_server' + customs[1] + '_' + str(customs[0]) + '.txt'
date = str(c_data.datetime.date(c_data.datetime.today()))


try:

    with open(log_name, 'a') as f:
       f.write(date+' '+nastroi[1]+' '+nastroi[0]+' admin Server activate\n')
       print('Начата запись в лог файл')
except FileNotFoundError:
    with open(log_name, 'w') as f:
        f.write(date+' '+nastroi[1]+' '+nastroi[0]+' admin Server activate\n')
        Print('Лог файл создан. Запись начата')
sock.listen(1)

def file_reader(name):
    file = open(name, 'r')
    content = file.read()
    file.close()
    return content

direct = os.getcwd()
while True:
    try:
        sockt = Web_server(*sock.accept(), direct)
        sockt.start()
    except:
        continue
