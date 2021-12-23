import socket
import time
from threading import Thread


def start_server():
    print('Starting the server...')
    sock = socket.socket()
    try:
        sock.bind(('', 80))
        print('Using port 80')
    except OSError:
        sock.bind(('', 8080))
        print('Using port 8080')
    sock.listen(5)
    print('The server has launched')
    while True:
        conn, addr = sock.accept()
        thread = Thread(target=proc, args=(conn, addr))
        thread.start()


filename = 'index.html'


def proc(conn, addr):
    h = (f'HTTP/1.1 200 OK\n'
         f'Server: Apache/2.2.17\n'
         f'Date: {time.asctime()}\n'
         f'Content-Type: text/html\n'
         f'Connection: close\n\n')
    try:
        user = conn.recv(1024).decode()
        print(user)
        path = user.split(' ')[1]
        if path == '/':
            with open(filename, 'rb') as f:
                conn.send(h.encode('utf-8') + f.read())
        else:
            conn.send('HTTP/1.1 404\nNOT FOUND'.encode('utf-8'))
    except IndexError:
        conn.send('HTTP/1.1 404\nNOT FOUND'.encode('utf-8'))
    print(addr, 'has connected')


if __name__ == '__main__':
    filename = input('Enter the path (absolute or relative) to an existing .html file: ')
    start_server()
