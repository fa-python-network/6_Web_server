import socket
import time
import json
import os
import threading
import logging


logging.basicConfig(filename='server.log', level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

sock = socket.socket()

with open("config.json", "r") as d:
    dataJSON = json.load(d)

try:
    sock.bind((dataJSON["Host"], dataJSON["Port"]))
    print(f'Using port {dataJSON["Port"]}')
except OSError:
    sock.bind((dataJSON["Host"], 8080))
    print('Using port 8080')

sock.listen(5)

def newclient (conn, addr, max, dir):
    while True:
        print("Connected", addr)

        data = conn.recv(max)
        msg = data.decode()
        msg = msg.split(' ')[1]
        msg = msg[1:]

        if msg == '':
            msg = 'index.html'

        if msg[-1] == '?':
            msg = msg[:-1]

        try:
            rash = msg.split('.')[1]
        except:
            rash = ''

        if rash not in ('html', 'css', 'js', 'min', 'png'):
            logging.info(f' {msg} - {addr[0]} - 403 forbidden')
            e = 403
            msg = '403.html'
        else:
            e = 200

        if rash == 'css' or rash == 'min':
            Content = "text/css"
        elif rash == 'html' or rash == 'htm':
            Content = "text/html"
        elif rash == 'png':
            Content = "image/png"
        elif rash == 'jpeg':
            Content = "image/jpeg"
        else:
            Content = ""

        try:
            logging.info(f'{msg} - {addr[0]} - 200 OK')
            with open(dir + msg, 'rb') as f:
                mess = f.read()
                leng = os.path.getsize(msg)


        except FileNotFoundError:
             e = 404
             logging.info(f'{msg} - {addr[0]} - 404')
             with open('404.htm', 'rb') as f:
                 mess = f.read()
                 leng = os.path.getsize('404.htm')


        resp = f"""HTTP/1.1 {e} OK
        Date: {time.ctime()}
        Server: SelfMadeServer v0.0.1
        Content-type: {Content}
        Content-Length: {leng}
        Connection: close

"""


        conn.send(resp.encode() + mess)
        conn.close()
        return
        
while True:
    conn, addr = sock.accept()
    t1 = threading.Thread(target=newclient, args=[conn, addr, dataJSON['Max'], dataJSON['Directory']])
    t1.start()