import os
from datetime import datetime
from socket import socket
from threading import Thread

import logger

typeDict = dict(html="text/html; charset=UTF-8", jpg="image/jpeg", css="text/css", ico="image/x-icon")


def get_date():
	return datetime.now().strftime("%a, %d %b 20%y %X GMT")


def check_date(addr, name, name_type) -> (bytes, int):
	request_type = None
	try:
		request_type = typeDict[name_type]
		code = "200 OK"
	except:
		code = "403 Forbidden"

	try:
		open(name).close()
		size = os.path.getsize(name)
	except:
		code = "404 Not found"
		size = 0
	resp = f"HTTP/1.1 {code}\n"
	resp += f"Date: {get_date()}\n"
	resp += f"Server: MyServer\n"

	if code.split()[0] == "200":
		resp += f"Content-type: {request_type}\n"

	if size != 0:
		resp += f"Content-Length: {size}\n"
	resp += "\n"

	logger.log(addr[0], name, code)

	return resp.encode(), int(code.split()[0])


def listen_to_client(conn, addr):
	while True:
		data = conn.recv(8192)
		msg = data.decode()
		name = msg.split()[1][1:]
		if name == "": name = "1.html"
		resp, code = check_date(addr, name, name.split('.')[-1])
		if code == 200:
			with open(name, "rb") as f:
				resp += f.read()
		elif code == 404:
			resp += "404 File not Found".encode()
		else:
			resp += "403 Forbidden File".encode()
		conn.send(resp)
		conn.close()


port = int(input("Порт:"))
sock = socket()

try:
	sock.bind(('', port))
except OSError:
	sock.bind(('', 8080))
sock.listen(5)
while True:
	conn, addr = sock.accept()
	print("Connected", addr)
	Thread(target=listen_to_client, args=(conn, addr)).start()
