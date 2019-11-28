import socket
import datetime
import os

def open_file(name):
    content = ''
    file = open(name,'r', encoding='utf-8')
    file.close()
    return content.encode()

sock = socket.socket()

try:
    sock.bind(('', 80))
    print("Using port 80")

except OSError:
    sock.bind(('', 8080))
    print("Using port 8080")


while True
    sock.listen(5)
    conn, addr = sock.accept()
    print("Connected", addr)

    data = conn.recv(8192)
    msg = data.decode()

    print(msg)
    try:
    	now = datetime.datetime.now()

        a = msg.split('\n')[0].split(' ')[1]
        s = os.path.exists(os.path.join(os.getcwd(), a[1:]))
        type = 'text/html'
        
        if s and a.split('.')[-1] == 'html':
            a = read_file(a[1:])
            type = 'text/html'
            state  = '200 OK'

        elif s and a.split('.')[-1] == 'jpg':
            a = read_img(a[1:])
            type = 'image/jpeg'

        elif s and a.split('.')[-1] == 'gif':
            a = read_img(a[1:])
            type = 'image/gif'

        elif s:
            state = '403'
            a = read_file('error403.html')
            type = 'text/html'

        elif not s:
            state = '404'
            a = read_file('error404.html')
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
    conn.send(resp.encode()+a)
    conn.close()

