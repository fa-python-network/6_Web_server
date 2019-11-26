import socket
from wsgiref.handlers import format_date_time
from datetime import datetime
from time import mktime
from os import path


def get(msg):
    msg_m = msg.split()
    if msg_m[1] == '/':
        msg_m[1] = '/index.html'
    try:
        with open('templates/'+msg_m[1][1:], 'r') as f:  # проверяем существование сего файлика
            htm = f.read()
    except:
        with open('templates/' + '404.html', 'r') as f:
            htm = f.read()
    return htm


def content_length(msg):
    msg_m = msg.split()
    if msg_m[1] == '/':
        msg_m[1] = '/index.html'
    try:
        with open('templates/' + msg_m[1][1:], 'r'):  # проверяем существование сего файлика
            return path.getsize('templates/' + msg_m[1][1:])
    except:
        return path.getsize('templates/' + '404.html')


sock = socket.socket()

try:
    sock.bind(('', 80))
    print("Using port 80")
except OSError:
    sock.bind(('', 8080))
    print("Using port 8080")

sock.listen(5)
while True:
    conn, addr = sock.accept()
    print("Connected", addr)

    data = conn.recv(8192)
    msg = data.decode()
    print(msg)
    now = datetime.now()
    stamp = mktime(now.timetuple())
    resp = ("""HTTP/1.1 200 OK
Server: SelfMadeServer v0.0.1
Date: {}
Content-type: text/html
Connection: close
Content-length: {}

"""+get(msg)).format(format_date_time(stamp), content_length(msg))

    conn.send(resp.encode())

    conn.close()
