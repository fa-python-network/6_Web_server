import socket
import datetime
import os
import time

dirname = os.getcwd()
st = open('settings.txt').readlines()
port = int(st[0][7::])
vol = int(st[2][6::])
log = open('log.txt', 'a+')

k = ''
try:
    if dirname.rstrip() == 'main':
        k = os.getcwd()
    else:
        k = os.path.join(os.getcwd(), dirname.rstrip())
except:
    k = os.path.join(os.getcwd(), dirname.rstrip())



sock = socket.socket()


sock.bind(('', port))
print("Using port " + str(port))

sock.listen(5)

conn, addr = sock.accept()
print("Connected", addr)

data = conn.recv(vol)
msg = data.decode()

print(msg)

tm = time.time()
tm = str(time.ctime(tm))

a = msg.split(' ')
ip = addr[0]
log.writelines('IP: ' + ip + '\n')
date = datetime.date.today()
log.writelines('Дата:' + str(date) + '\n')
a1 = a[1]
add = a1[1::]
try:
    pnt = add.split('.')
    pnt = pnt[1].rstrip()
except:
    pnt = ''

if add == '':
    log.writelines('Req without files' + '\n')
else:
    log.writelines('Запрошенный файл: ' + add + '\n')

try:
    if add.rstrip() == '':
        tt = os.path.join(k, 'index.html')
        tt = tt.replace('\\','/')
        with open(tt, 'r', encoding='utf-8') as f: 
            s = ''
            s1 = ''
            for i in f:
                s1 += i
                s += i
            s1 = len(s1)
        resp = f"""HTTP/1.1 200 OK
        {tm}
        Server: SelfMadeServer v0.0.2
        Content-type: text/html
        {s1}
        Connection: close

{s}"""

    elif  pnt != 'html' and pnt != 'js' and pnt != 'css':
        resp = f"""HTTP/1.1 403 Forbidden
        Server: SelfMadeServer v0.0.2
        Content-type: text/html
        Connection: close"""

    else:
        tt = os.path.join(k, add)
        with open(tt, 'r', encoding='utf-8') as f:
            s = ''
            s1 = ''
            for i in f:
                s1 += i
                s += i
            s1 = len(s1)
        resp = f"""HTTP/1.1 200 OK
        {tm}
        Server: SelfMadeServer v0.0.2
        Content-type: text/html
        {s1}
        Connection: close

{s}"""
except FileNotFoundError:
    resp = f"""HTTP/1.1 404 Not Found
        {tm}
        Server: SelfMadeServer v0.0.2
        Content-type: text/html
        {s1}
        Connection: close"""




conn.send(resp.encode())
mskt = resp.split(' ')
mskt1 = mskt[1]
if int(mskt1) >= 400:
    log.writelines('Ошибка: ' + mskt1 + '\n' + '\n')

conn.close()
log.close()