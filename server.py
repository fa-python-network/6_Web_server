import socket
import time
import json
import os
import threading
import logging

logging.basicConfig(filename='server.log', level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

sock = socket.socket()

with open("config.json", "r") as f:
    global config
    config = json.load(f)

try:
    sock.bind(('', config["port"]))
    print(f"Using port {config['port']}")
except OSError:
    sock.bind(('', 8080))
    print("Using port 8080")

sock.listen(5)

def work(msg, conn, addr):
    print("Connected", addr)

    rash = msg.split('.')[1]
    if rash not in ('html','css','js', 'min'):
        logging.info(f' {msg} - {addr[0]} - 403 forbidden')
        status = "HTTP/1.1 403 forbidden\n"
        msg = '403.html'
    else:
        logging.info(f'{msg} - {addr[0]} - 200 OK')
        status = "HTTP/1.1 200 OK\n"

    file = ''
    try:
        with open(os.path.join(config["dir"], msg), 'r') as f:
            for line in f:
                file += line
    except FileNotFoundError:
        logging.info(f'{msg} - {addr[0]} - 404 NOT FOUND')
        status = "HTTP/1.1 404 NOT FOUND\n"
        with open(os.path.join(config["dir"], "404.html"), 'r') as f:
            for line in f:
                file += line
    
    date = f'Date: {time.ctime()}\n'
    print(msg)

    resp = ""
    resp += status
    resp += f'Server: SelfMadeServer v0.0.1\n'
    resp += date
    resp += "Content-type: text/html\n"
    resp += f'Content-length: {len(file.encode())}\n\n'
    print(resp)
    resp += file
    resp += 'Connection: close'
    
    conn.send(resp.encode())

    conn.close()

while True:
    conn, addr = sock.accept()

    data = conn.recv(config["bite"])
    msg = data.decode()
    msg = msg.split(' ')[1]
    msg = msg[1:]

    if msg == 'favicon.ico':
        continue

    if msg == '':
        msg = '1.html'

    t1 = threading.Thread(target=work, args=[msg, conn, addr])
    t1.start()