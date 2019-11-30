import datetime
import socket
import threading
import logging
from settings import *
import os

files_in_directory=os.listdir() #список файлов в директории


def process(conn, addr):
    print("Connected", addr)

    data = conn.recv(REQUEST_LENGTH)
    msg = data.decode()

    print(msg)
    msg_ = msg.split(' ')
    file=msg_[1][1:]
    answer=''
    resp=''

    if '.' in file:
        if file in files_in_directory and file.split('.')[1] in ALLOWED_FORMATS:
            with open(file, 'r', encoding="UTF-8") as f:
                answer = f.read()
            size = os.path.getsize(file)

            resp = f"""HTTP/1.1 200 OK
			Date: {get_date()}
			Server: SelfMadeServer v0.0.1
			Content-length: {size}
			Content-type: text/html
			Connection: close

			{answer}
			"""
        elif file not in files_in_directory:
            file="404.html"
            with open(file, 'r', encoding="UTF-8") as f:
                answer = f.read()
            size = os.path.getsize(file)

            resp = f"""HTTP/1.1 200 OK
            Date: {get_date()}
   			Server: SelfMadeServer v0.0.1
   			Content-length: {size}
			Content-type: text/html
            Connection: close

            {answer}
            """
        elif file.split('.')[1]  not in ALLOWED_FORMATS:
            file = "403.html"
            with open(file, 'r', encoding="UTF-8") as f:
                answer = f.read()
            size = os.path.getsize(file)

            resp = f"""HTTP/1.1 200 OK
            Date: {get_date()}
            Server: SelfMadeServer v0.0.1
            Content-length: {size}
            Content-type: text/html
            Connection: close

            {answer}
            """

    else:
        file = "404.html"
        with open(file, 'r', encoding="UTF-8") as f:
            answer = f.read()
        size = os.path.getsize(file)

        resp = f"""HTTP/1.1 200 OK
        Date: {get_date()}
        Server: SelfMadeServer v0.0.1
        Content-length: {size}
        Content-type: text/html
        Connection: close

        {answer}
        """

    try:
        resp_ = resp.split()
        error_number = resp_[1]
        serv_log.info(f"{get_date()} {addr} {file} {error_number}")

    except Exception as e:
        pass


    conn.send(resp.encode())

    conn.close()


def get_date():
    return datetime.datetime.now()


sock = socket.socket()

try:
    sock.bind(('', PORT))
    print("Using port 80")
except OSError:
    sock.bind(('', 8080))
    print("Using port 8080")

sock.listen(5)

serv_log = logging.getLogger('log_')
serv_log_handler = logging.FileHandler('server.log', encoding='UTF-8')
serv_log_handler.setLevel(logging.INFO)
serv_log.addHandler(serv_log_handler)
serv_log.setLevel(logging.INFO)

while True:
    conn, addr = sock.accept()
    threading.Thread(target=process, args=[conn, addr]).start()
