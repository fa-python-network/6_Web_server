import os
import socket
from datetime import datetime
from threading import Thread


typeDict = dict(html="text/html; charset=UTF-8", jpg="image/jpeg", css="text/css", ico="image/x-icon")

def getDate():
	return datetime.now().strftime("%a, %d %b 20%y %X GMT")

def checkType(name, nameType) -> str:
	try:
		requestType = typeDict[nameType]
		resp = f"HTTP/1.1 200 OK\n"
	except:
		requestType = nameType
		date = getDate()
		resp = f"""HTTP/1.1 403 Forbidden
		
Date: {date}
Server: MyServer

"""
		return resp.encode()
	date = getDate()
	size = os.path.getsize(name)
	resp += f"""Date: {date}
Server: MyServer
Content-type: {requestType}
Content-Length: {size}

"""
	return resp.encode()

def listenToClient(conn, addr):
	data = conn.recv(8192)
	msg = data.decode()
	name = msg.split()[1][1:]
	if name == "": name = "1.html"
	resp = checkType(name, name.split('.')[-1])
	try:
		with open(name, "rb") as f:
			resp += f.read()
	except:
		resp += "403 Forbidden Format".encode()
	conn.send(resp)
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
	Thread(target=listenToClient, args=(conn, addr)).start()
