import socket
import re
import time
import logging
import threading
from config import *

http_request_finder = re.compile(r"(GET|POST) (/.*) (HTTP/1\.1)")
file_finder = re.compile(r"^/(.*)\.(html|css|jpg|png|ico)(/|)$")


def get_response(request_header, addr):
    if request_header.group(1) == "GET":
        file_groups = file_finder.match(request_header.group(2))
        if file_groups is not None:
            try:
                response = eval(f"get_{file_groups.group(2)}(\"{'.'.join(file_groups.group(1,2))}\")")
            except NameError as e:
                server_log.info(f"{time.asctime(time.gmtime(time.time()))} {addr} {request_header.group(2)} 403")
                return resp_403()
            except FileNotFoundError as e:
                server_log.info(f"{time.asctime(time.gmtime(time.time()))} {addr} {request_header.group(2)} 404")
                return resp_404('.'.join(file_groups.group(1,2)))
            server_log.info(f"{time.asctime(time.gmtime(time.time()))} {addr} {request_header.group(2)} 200")
            return response
        else:
            server_log.info(f"{time.asctime(time.gmtime(time.time()))} {addr} {request_header.group(2)} 403")
            return resp_403()
    server_log.info(f"{time.asctime(time.gmtime(time.time()))} {addr} {request_header.group(2)} 400")
    return resp_400()


def get_html(filename):
    resp = f"""HTTP/1.1 200 OK
    Date: {time.asctime(time.gmtime(time.time()))}
    Server: SelfMadeServer v0.0.1
    Content-type: text/html

    """
    with open(filename, "r") as f:
        for i in f.readlines():
            resp += i
    return resp


def get_css(filename):
    resp = f"""HTTP/1.1 200 OK
    Date: {time.asctime(time.gmtime(time.time()))}
    Server: SelfMadeServer v0.0.1
    Content-type: text/css

    """
    with open(filename, "r") as f:
        for i in f.readlines():
            resp += i
    return resp


def resp_404(page):
    resp_not_found = f"""HTTP/1.1 404 Not Found
        Date: {time.asctime(time.gmtime(time.time()))}
        Server: SelfMadeServer v0.0.1
        Content-type: text/html
        Connection: close

        """
    with open("404.html", "r") as f:
        for i in f.readlines():
            resp_not_found += i.format(page)
    return resp_not_found


def resp_403():
    resp_forbidden = f"""HTTP/1.1 403 Forbidden
            Date: {time.asctime(time.gmtime(time.time()))}
            Server: SelfMadeServer v0.0.1
            Content-type: text/html
            Connection: close

            """
    with open("403.html", "r") as f:
        for i in f.readlines():
            resp_forbidden += i

    return resp_forbidden


def resp_400():
    resp_bad_request = f"""HTTP/1.1 400 Bad Request
        Date: {time.asctime(time.gmtime(time.time()))}
        Server: SelfMadeServer v0.0.1
        Content-type: text/html
        Connection: close

        """
    with open("400.html", "r") as f:
        for i in f.readlines():
            resp_bad_request += i
    return resp_bad_request


def work(conn, addr):
    print("Connected", addr)
    data = conn.recv(MAX_REQUEST_LENGTH)
    msg = data.decode()

    print(msg)

    resp = http_request_finder.match(msg)

    if resp is not None:
        resp = get_response(resp, addr)
    else:
        resp = resp_400()

    print("-----------------------------------")
    print(resp)
    conn.send(resp.encode())
    print("Отправил!")
    conn.close()

sock = socket.socket()
try:
    sock.bind(('', PORT))
    print("port 80")
except OSError:
    sock.bind(("", PORT2))
    print("port 8080")

sock.listen(5)

server_log = logging.getLogger('logger')
server_log_handler = logging.FileHandler('server.log', encoding='UTF-8')
server_log_handler.setLevel(logging.INFO)
server_log.addHandler(server_log_handler)
server_log.setLevel(logging.INFO)

while True:
    print("Опять жду!")
    conn_, addr_ = sock.accept()
    threading.Thread(target=work, args=[conn_, addr_]).start()
