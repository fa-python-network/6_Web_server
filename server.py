import socket
import datetime
import os


def open_file(name):
    content = ''
    file = open(name, 'r', encoding='utf-8')
    file.close()
    return content.encode()



def open_img(name):
    f = open(name, 'rb')
    c = f.read()
    f.close()
    return c



sock = socket.socket()


try:
    sock.bind(('', 90))
    print("Using port 90")


except OSError:
    sock.bind(('', 8090))
    print("Using port 8090")


while True:
    sock.listen(5)
    conn, addr = sock.accept()
    print("Connected", addr)


    data = conn.recv(8192)
    msg = data.decode()


    print(msg)
    try:

        a = msg.split('\n')[0].split(' ')[1]
        s = os.path.exists(os.path.join(os.getcwd(), a[1:]))
        type = 'text/html'
        time = datetime.datetime.now()
        if s and a.split('.')[-1] == 'html':
            a = open_file(a[1:])
            type = 'text/html'
            state = '200 OK'

        elif s and a.split('.')[-1] == 'jpg':
            a = open_img(a[1:])
            type = 'image/jpeg'

        elif s and a.split('.')[-1] == 'gif':
            a = open_img(a[1:])
            type = 'image/gif'

        elif s:
            state = '403'
            a = open_file('error403.html')
            type = 'text/html'

        elif not s:
            state = '404'
            a = open_file('error404.html')
            type = 'text/html'

        else:
            a = a.encode()

        resp = f""""HTTP/1.1 {state}
Server: SelfMadeServer v0.0.1
Content-type: {type}
Content-length{len(a)}
Date: {time}
Connection: close
"""
    except IndexError:
        pass
    conn.send(resp.encode() + a)
    conn.close()
