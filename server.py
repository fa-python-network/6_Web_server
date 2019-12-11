import socket
from wsgiref.handlers import format_date_time
from datetime import datetime
from time import mktime
import os
from threading import Thread
import time

TYPEDICT = {"html" : "text/html; charset=UTF-8",
        "jpg" : "image/jpeg",
        "css" : "text/css",
        "ico" : "image/x-icon"}

def Dateget():
    now = datetime.now()
    stamp = mktime(now.timetuple())
    return format_date_time(stamp)

def checkType(name,nameType):
    resp = ""
    requestType = ""
    try:
        requestType = TYPEDICT[nameType]
        resp += f"HTTP/1.1 200 OK\n"
    except: 
        requestType = nameType
        resp += f"HTTP/1.1 403 Forbidden\n"
    date = Dateget()
    size = os.path.getsize(name)
    resp += f"""Date: {date}
    Server: MyServer
    Content-type: {requestType}
    Content-Length: {size}
    Connection: close

     """ 
    return resp

def listenToClient(conn,addr):
        data = conn.recv(8192)
        msg = data.decode()

        name = msg.split()[1][1:]
        if name == "" : name = "g1.html"
        resp = checkType(name,name.split('.')[-1])
        with open(name, "r") as f:
	        resp += f.read()
        conn.send(resp.encode())
        print(Dateget())
        conn.close()

port = int(input("Порт:"))
sock = socket.socket()
try:
    sock.bind(('', port))
except OSError:
    sock.bind(('', 8080))
sock.listen(5)
while True:
    conn, addr = sock.accept()
    print("Connected", addr)
    Thread(target = listenToClient,args = (conn,addr)).start()

