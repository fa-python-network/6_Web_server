import socket
import logging
from threading import *

logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s | %(levelname)s | %(message)s",
            handlers=[
                logging.FileHandler("server.log"),
                logging.StreamHandler(),
            ],
        )
with open('settings.txt') as f:
    for line in f:
        HOST = line.split(';')[0]
        PORT = int(line.split(';')[1])
        max_size = int(line.split(';')[2])
with open('favicon.png', 'rb') as file:
    x = file.open()

sock = socket.socket()
with open('temp/index.html') as file:
    htm1 = file.read()
error404header = 'HTTP/1.1 404 Not Found' + x
error403header = 'HTTP/1.1 403 Forbidden Error'

try:
    sock.bind((HOST, PORT))
    print("Using port ", PORT)
except OSError:
    sock.bind(('', 8080))
    print("Using port 8080")

sock.listen(5)

def new_client(conn, addr):
    print("Connected", addr)

    data = conn.recv(max_size)
    msg = data.decode()
    msg1 = msg.split(" ")[1]

    try:
        msg = msg1.split('.')
    except:
        pass

    if len(msg) == 1 or msg[1] == 'html' or msg[1] == 'js' or msg[1] == 'css':
        response(msg,msg1)
    else:
        resp = """HTTP/1.1 403 Forbidden
Server: SelfMadeServer v0.0.1
Content-type: text/html
Connection: close

""" + error403header
        logging.error(f'{addr[1]}, {msg1[1:]} raised Error 403 ')
        conn.send(resp.encode())

def response(msg,msg1):
    try:
        with open('temp/' + msg1[1:]) as file:
            htm = file.read()
        resp = """HTTP/1.1 200 OK
Server: SelfMadeServer v0.0.1
Content-type: text/html
Connection: close

"""+htm
    except:
        resp = """HTTP/1.1 404 Not Found
Server: SelfMadeServer v0.0.1
Content-type: text/html
Connection: close

"""+error404header

        logging.error(f'{addr[1]}, {msg1[1:]} raised Error 404 ')
    finally:
        if msg1[1:] == "":
            resp = """HTTP/1.1 200 OK
Server: SelfMadeServer v0.0.1
Content-type: text/html
Connection: close

"""+htm1

    print(msg)
    conn.send(resp.encode())



while True:
	conn, addr = sock.accept()
	Thread(target=new_client, args=(conn, addr)).start()

conn.close()
