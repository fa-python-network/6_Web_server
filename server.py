import socket
import os

PORT = 8085

sock = socket.socket()
sock.bind(('', PORT))
sock.listen()
print("Прослушиваем порт", PORT)

def readed_file(path):
    try:
        f = open('docs' + path, 'r')
    except OSError:
        return ""

    str = ''
    for line in f:
        str += line
    return str

while True:
    conn, addr = sock.accept()
    
    request = conn.recv(8192).decode().split('\n\n')

    header = request[0]
    header = header.split('\n')

    path = (header[0].split())[1]

    if path == "/":
        path = '/index.html'

    headers_to_res = "HTTP/1.0 200 OK\n\n"
    body = readed_file(path)
    if body == "":
        conn.send("HTTP/1.0 404 BAD_REQEST\n\n BAD REQEST".encode())
    else:
        res = headers_to_res + body
        conn.send(res.encode())

    conn.close()
