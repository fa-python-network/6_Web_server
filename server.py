import socket
import os
import logging

sock = socket.socket()
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

#  Создается и используется объект логгирования
logger = logging.getLogger("serverLogger")
logger.setLevel(logging.INFO)
fh = logging.FileHandler("server.log")
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

try:
    sock.bind(('', 80))
    print("Using port 80")
except OSError:
    sock.bind(('', 7777))
    print("Using port 7777")

sock.listen(1)
conn, addr = sock.accept()
print("Connected", addr)

data = conn.recv(8192)
msg = data.decode()

try:
    with open(os.getcwd()+(msg.split(' '))[1], 'r', encoding='utf-8') as f:
        inner = f.read()
        if (msg.split(' '))[1].split('.')[-1] in ['html', 'css', 'js']:
            resp = """HTTP/1.1 200 OK
Server: SelfMadeServer v0.0.1
Content-type: text/html
Connection: close

""" + inner
            form = 200
        else:
            resp = """HTTP/1.1 403 Forbidden
Server: SelfMadeServer v0.0.1
Content-type: text/html
Connection: close

"""
            form = 403
except:
    if len((msg.split(' '))[1]) == 1:
        with open(os.path.join(os.getcwd(), 'index.html'), 'r', encoding='utf-8') as f:
            inner = f.read()
        resp = """HTTP/1.1 200 OK
Server: SelfMadeServer v0.0.1
Content-type: text/html
Connection: close

""" + inner
        form = 200
    else:
        resp = """HTTP/1.1 404 Not Found
Server: SelfMadeServer v0.0.1
Content-type: text/html
Connection: close

"""
        form = 404

logger.info(f"{addr[0]} {msg.split(' ')[1]} {form}")
conn.send(resp.encode())
conn.close()
