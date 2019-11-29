import socket
import re

head = ['HTTP/1.1 200 OK', 'Server: Pokekek 0.02', 'Content-type: text/html', 'Connection: close', '', '']
PAT = re.compile(r'[A-Z]{3,6}\s[\S]*\sHTTP/[0-9.]*', flags=re.MULTILINE) 
htmllist = ['index.html', 'favicon.ico']


class Response:
    def __init__(self, html ):
        self.head = head
        if html[1:] in htmllist:
            if 'favicon.ico' in html:
                self.head[2] = 'Content-type: image/ico'
            with open(html[1:], 'rb') as file:
                self.html = file.read()
        elif html == '/':
            with open('index.html', 'rb') as file:
                self.html = file.read()
        else:
            with open('322.html', 'rb') as file:
                self.html = file.read()
                self.head[0] = 'HTTP/1.1 404 Not Found'

    
    def __str__(self):
        return '\n'.join(self.head)

    def __call__(self):
        return str(self).encode('UTF-8') + self.html


def parse(req):
    return PAT.findall(req)[0].split(' ')[1]


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
    if msg:
        html = parse(msg)
    conn.send(Response(html)())

    conn.close()