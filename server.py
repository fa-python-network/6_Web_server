import socket, time
from threading import Thread


def server():
    print('Launching the server...')
    sock = socket.socket()
    try:
        sock.bind(('', 80))
        print("Using port 80")
    except OSError:
        sock.bind(('', 8080))
        print("Using port 8080")
    sock.listen(10)
    print('Success!')
    while 1:
        conn, addr = sock.accept()
        thread = Thread(target=proc, args=(conn, addr,))
        thread.start()


name = input('Enter a full name of an existing .html file (Example: index.html): ')


def proc(conn, addr):
    h = (f'HTTP/1.1 200 OK\n'
         f'Server: SelfMadeServer v0.0.1\nDate: {time.asctime()}\nContent-Type: text/html\nConnection: close\n\n')
    user = conn.recv(1024).decode()
    path = user.split(" ")[1]
    if path == '/':
        with open(name, 'rb') as f:
            answer = f.read()
            conn.send(h.encode('utf-8') + answer)
    else:
        resp = """HTTP/1.1 404
            NOT FOUND"""
        conn.send(resp.encode('utf-8'))
    print(addr, ' has connected')


if __name__ == "__main__":
    server()