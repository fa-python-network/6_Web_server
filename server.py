import socket
from threading import Thread
from datetime import datetime

def server():
    sock = socket.socket()
    try:
        sock.bind(('', 80))
        print("Запуск сервера")
    except OSError:
        sock.bind(('', 8080))
    sock.listen(5)
    while True:
        conn, addr = sock.accept()
        print("Connected", addr)
        thread = Thread(target=web_page, args=(conn, addr,))
        thread.start()

def web_page(conn, addr):
    resp = f'HTTP/1.1 200 OK\n\
        Server: SelfMadeServer v0.0.1\n\
        Date: {datetime.now()}\n\
        Content-Type: text/html\n\
        Connection: close\n\n'
    user = conn.recv(1024).decode()
    path = user.split(" ")[1]
    if path == '/' or path == '/index.html':
        with open('index.html', 'rb') as file:
            answer = file.read()
            conn.send(resp.encode('utf-8') + answer)
    else:
        conn.send(("Error: 404").encode('utf-8'))

if __name__ == "__main__":
    server()
