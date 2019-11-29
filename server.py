import socket
from settings import Settings
import threading
import datetime
import os

sock = socket.socket()

try:
    sock.bind(('', 80))
    print("Using port 80")
except OSError:
    sock.bind(('', 8080))
    print("Using port 8080")
def request(conn, addr, data, directory):
    
    msg = data.decode()
    print(msg)

sock.listen(5)

name = msg.split()[1][1:]

conn, addr = sock.accept()
print("Connected", addr)
if name == "":
        name = "index.html"
name = directory + "\\" + name


now = datetime.datetime.now()
date = now.strftime("%a, %d %b %Y %H:%M:%S GTM")

    
with open("log.txt", "a") as log:
        print(f"Date: {date}\nAddr: {addr}\nFile: {name}", file=log)

    
try:
        size = os.path.getsize(name)  

  
except FileNotFoundError:
        resp = f"""HTTP/1.1 404 Not Found
        Server:SelfMadeServer v0.0.1
        Date: {date}
        Connection: keep-alive
        """
        with open("log.txt", "a") as log:
            print("Error: 404", file=log)

data = conn.recv(8192)
msg = data.decode()
resp = resp.encode()
    else:
        decr = name.split(".")[-1]  
        if decr not in settings.types:
            resp = f"""HTTP/1.1 403 Forbidden
            Server:SelfMadeServer v0.0.1
            Date: {date}
            Connection: keep-alive
            """
            with open("log.txt", "a") as log:
                print("Error: 403", file=log)
        else:
            try:
                with open(name, "r", encoding="utf-8") as file:
                    resp = f"""HTTP/1.1 200 OK
                    Server: SelfMadeServer v0.0.1
                    Date: {date}
                    Content-Type: text/{decr};charset=utf-8
                    Content-Length: {size}
                    Connection: keep-alive
print(msg)
                    """
                    resp += file.read()
                resp = resp.encode() 
def connection(conn, addr, directory):
    data = conn.recv(settings.request_size)
    if not data:
        return
    request(conn, addr, data, directory)
    conn.close()

conn.close() 

settings = Settings() 
sock = socket.socket()


try:
    sock.bind(('', settings.port))
    print(f"Using port {settings.port}")
except OSError:
    sock.bind(('', settings.port2))
    print(f"Using port {settings.port2}")
sock.listen(5)

directory = settings.directory


conn, addr = sock.accept()
while True:
    print("Connected", addr, "\n")
    tr = threading.Thread(target=connection, args=(conn, addr, directory))
    tr.start()
    conn, addr = sock.accept() 
