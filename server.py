import datetime as d
import os
from contextlib import closing
import socket
import threading

def logging (name, errorc, date, ipe):#, nom
    f = open(log_nam, 'a')
    f.write(date+' '+ipe+' '+name+' '+errorc+'\n')
    f.close()
def find_free_port(nastroip):
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind((nastroip, 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]
def file_reader(name):
    file = open(name, 'r')
    content = file.read()
    file.close()
    return content

nastroi=[]
with open ('nastroy.txt', 'r') as f:
    for i in f:
        nastroi.append(i.split(': ')[1][:-1])
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
nastroi[0]=int(nastroi[0])
nastroi[2]=int(nastroi[2])
try:
    sock.bind((nastroi[1], nastroi[0]))
    print(f"Ваш адрес {nastroi[1]} {nastroi[0]}")
except OSError:
    nastroi[0] = find_free_port(nastroi[1])
    print('Ошибка. Выбранный код сервера занят, код сервера будет изменён автоматически. Новый код: ',nastroi[1], nastroi[0])
    sock.bind(('', nastroi[0]))
nastroi[0]=str(nastroi[0])
log_nam = 'log_server'+nastroi[1]+'_'+str(nastroi[0])+'.txt'
date=str(d.datetime.date(d.datetime.today()))
try:
    with open (log_nam, 'a') as f:
        f.write(date+' '+nastroi[1]+' '+nastroi[0]+' admin Server activate\n')
except FileNotFoundError:
    with open (log_nam, 'w') as f:
        f.write(date+' '+nastroi[1]+' '+nastroi[0]+' admin Server activate\n')
sock.listen(1)

class ConnectionW(threading.Thread):
    def __init__(self, conn, addr, direct):
        super().__init__(daemon=True)
        self.conn = conn
        self.addr = addr
        self.ipe = str(addr)
        self.hello()
        self.direct=direct
        self.work_sun_is_high()

    def hello(self):
        print("Connected", self.addr)
    def work_sun_is_high(self):
        while True:
            try:
                fl = self.conn.makefile('r')
            except ConnectionAbortedError:
                break
            msg = fl.readline(nastroi[2]).split()[1]
            if msg == '/':
                msg='/index.html'
                typfi = 'html'
            else:
                try:
                    typfi=msg.split('.')[-1]
                except IndexError:
                    typfi='-'
            fl=os.path.join(self.direct, msg[1:])
            if os.path.exists(fl) == True:
                if typfi == 'txt' or typfi == 'html':
                    typfi='text/html'
                    self.otprav(file_reader(fl), msg, typfi, 'non_error')
                    '''elif typfi == 'img':#'''

                    '''ошибка 403'''
                else:
                    self.otprav("Error 403.  The format is not supported", msg, typfi, '403')
            else:
                self.otprav("Error 404. File not found", msg, typfi, '404')#'''

        self.conn.close()
    def otprav(self, resp, msg, typfi, err):
        date = str(d.datetime.date(d.datetime.today()))
        logging(msg, err, date, self.ipe)
        ln_res=len(resp)
        resp = f"""HTTP/1.1 200 OK
Server: SelfMadeServer v0.0.1
Content-type: {typfi}
Date: {date}
Connection: close
Date: {date}
Content-length: {ln_res}
{resp}"""
        self.conn.send(resp.encode('utf-8'))

direct=os.getcwd()
while True:
        try:
            potok = ConnectionW(*sock.accept(), direct)
            potok.start()
        except:
            continue 
