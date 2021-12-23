import socket
from threading import Thread
import time
def create_server():
    sock = socket.socket()
    sock.bind(('', 80))
    print("Server is on")
    sock.listen(5)
    while True:
        conn, addr = sock.accept()
        thread = Thread(target=work, args=(conn, addr,))
        thread.start()


def work(conn, addr):
    print("Joined", addr)
    t = time.asctime(time.gmtime()).split(' ')
    t = f'{t[0]}, {t[2]} {t[1]} {t[4]} {t[3]}'
    print("Date: ", t)
    h = f'HTTP/1.1 200 OK\nServer: SelfMadeServer v0.0.1\nDate: {t}\nContent-Type: text/html; charset=utf-8\nConnection: close\n\n'
    user = conn.recv(1024).decode()
    rez = user.split(" ")[1]
    if rez == '/' or rez == '/index.html':
        with open('index.html', 'rb') as f:
            answer = f.read()
            conn.send(h.encode('utf-8') + answer)
    elif rez == "/1.html":
        with open('1.html', 'rb') as f:
            answer = f.read()
            conn.send(h.encode('utf-8') + answer)
    else:
        resp = """HTTP/1.1 200 OK
            NOT FOUND"""
        conn.send(resp.encode('utf-8'))


if __name__ == "__main__":
    create_server()
