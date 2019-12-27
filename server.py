import socket
import os
import datetime
import logging
from threading import Thread

from settings import Settings  


def handler(msg):
    _, url = msg.split(" ")[:2]  
    file_type = url.split(".")[-1]  
    date = datetime.datetime.now().strftime('%a, %d %b %Y %H:%M:%S GTM')  
    if os.path.isfile(Settings.directory + url):  
        if file_type in Settings.types:  
            with open(Settings.directory + url, "rb") as sf:
                data = sf.read()
                return f"HTTP/1.1 200\n" \
                       f"Server: {Settings.name}\n" \
                       f"Date: {date}\n" \
                       f"Content-length: {len(data)}\n" \
                       f"Content-type: {Settings.types[file_type]}\n" \
                       f"Connection: keep-alive\n" \
                       f"\r\n\r\n".encode() + data 
        else:  # Если не поддерживается, 403
            return f"HTTP/1.1 403\n" \
                   f"Server: {Settings.name}\n" \
                   f"Date: {date}\n" \
                   f"Content-type: text/html; charset=UTF-8\n" \
                   f"Connection: keep-alive\n" \
                   f"\r\n\r\n".encode()  + "<h1>403</h1>".encode()
    # Если файла нет,  404 Не найдено
    return f"HTTP/1.1 404\n" \
            f"Server: {Settings.name}\n" \
            f"Date: {date}\n" \
            f"Content-type: text/html; charset=UTF-8\n" \
            f"Connection: keep-alive\n" \
            f"\r\n\r\n".encode() + "<h1>404</h1>".encode()


def connection(conn, addr):
    while True: 

        data = conn.recv(Settings.request_size)  

        if data == b"":  
            conn.close()
            break

        msg = data.decode()  

        logging.info(str(addr[0]) + ":" + str(addr[1]) + " новый запрос") 

        resp = handler(msg)  

        conn.send(resp)  


if __name__ == '__main__':  

    logging.basicConfig(  
        level=logging.DEBUG,
        format="%(asctime)s | %(levelname)s | %(message)s",
        handlers=[
            logging.FileHandler("logs.log"),
            logging.StreamHandler(),
        ],
    )

    sock = socket.socket()  
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  

    sock.bind(('', Settings.port)) 
    logging.info("Запуск сервер на порте: " + str(Settings.port))

    sock.listen(0)  

    while True:  
        conn, addr = sock.accept() 
        logging.info("Новое подключение: " + str(addr[0]) + ":" + str(addr[1]))  
        flow = Thread(target=connection, args=(conn, addr))  
        flow.start()
