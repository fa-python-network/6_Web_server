import socket
import re
from config import *

http_request_finder = re.compile(r"(GET|POST) (/.*) (HTTP/1\.1)")
file_finder = re.compile(r"^/(.*)\.(html|css|jpg|png|ico)(/|)$")


def get_response(request_header):
    if request_header.group(1) == "GET":
        file_groups = file_finder.match(request_header.group(2))
        if file_groups is not None:
            try:
                response = eval(f"get_{file_groups.group(2)}(\"{'.'.join(file_groups.group(1,2))}\")")
            except NameError as e:
                return resp_403()
            except FileNotFoundError as e:
                return resp_404()
            return response
        else:
            return resp_403()
    return resp_404()


def get_html(filename):
    resp = """HTTP/1.1 200 OK
    Server: SelfMadeServer v0.0.1
    Content-type: text/html

    """
    with open(filename, "r") as f:
        for i in f.readlines():
            resp += i
    return resp


def get_css(filename):
    resp = """HTTP/1.1 200 OK
    Server: SelfMadeServer v0.0.1
    Content-type: text/css

    """
    with open(filename, "r") as f:
        for i in f.readlines():
            resp += i
    return resp


def resp_404():
    resp_not_found = """HTTP/1.1 404 Not Found
        Server: SelfMadeServer v0.0.1
        Content-type: text/html
        Connection: close

        """
    with open("404.html", "r") as f:
        for i in f.readlines():
            resp_not_found += i
    return resp_not_found


def resp_403():
    resp_forbidden = """HTTP/1.1 403 Forbidden
        Server: SelfMadeServer v0.0.1
        Content-type: text/html
        Connection: close

        """
    with open("403.html", "r") as f:
        for i in f.readlines():
            resp_forbidden += i
    return resp_forbidden

sock = socket.socket()
try:
    sock.bind(('', PORT))
    print("port 80")
except OSError:
    sock.bind(("", PORT2))
    print("port 8080")

sock.listen(5)

while True:
    print("Опять жду!")
    conn, addr = sock.accept()
    print("Connected", addr)
    data = conn.recv(8192)
    msg = data.decode()

    print(msg)


    resp = http_request_finder.match(msg)
    if resp is not None:
        resp = get_response(resp)
    else:
        resp = resp_400()

    print("-----------------------------------")
    print(resp)
    conn.send(resp.encode())
    print("Отправил!")
    conn.close()
