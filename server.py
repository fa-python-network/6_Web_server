import socket
import time
import threading
import logging
from config import *

def process(conn,addr):
	print("Connected", addr)

	data = conn.recv(REQUEST_LENGTH)
	msg = data.decode()

	print(msg)
	msg_ = msg.split()
	file_name = msg_[1]

	if '.' in file_name:
		if file_name.split('.')[1] in ALLOWED_FORMATS:

			if "GET /index.html HTTP/1.1" in msg:
				resp_body=""

				length=0
				with open ('index.html', 'r') as f:
					for i in f.readlines():
						length+=len(i)
						resp_body+=i

				resp = f"""HTTP/1.1 200 OK
				Date: {get_date()}
				Server: SelfMadeServer v0.0.1
				Content-length: {length}
				Content-type: text/html
				Connection: close

				{resp_body}
				"""
			else:
				resp_body=""

				length=0
				with open ('404.html', 'r') as f:
					for i in f.readlines():
						length+=len(i)
						resp_body+=i

				resp = f"""HTTP/1.1 404 Not Found
				Date: {get_date()}
				Server: SelfMadeServer v0.0.1
				Content-length: {length}
				Content-type: text/html
				Connection: close

				{resp_body}
				"""
		else:
			resp_body=""

			length=0
			with open ('403.html', 'r') as f:
				for i in f.readlines():
					length+=len(i)
					resp_body+=i

			resp = f"""HTTP/1.1 403 Forbidden
			Date: {get_date()}
			Server: SelfMadeServer v0.0.1
			Content-length: {length}
			Content-type: text/html
			Connection: close

			{resp_body}
			"""
	else:
		resp_body=""

		length=0
		with open ('404.html', 'r') as f:
			for i in f.readlines():
				length+=len(i)
				resp_body+=i

		resp = f"""HTTP/1.1 404 Not Found
		Date: {get_date()}
		Server: SelfMadeServer v0.0.1
		Content-length: {length}
		Content-type: text/html
		Connection: close

		{resp_body}
		"""
	try:
		resp_ = resp.split()
		error_number = resp_[1]
		serv_log.info(f"{get_date()} {addr} {file_name} {error_number}")
		
	except Exception as e:
		pass	

	print("-"*15)
	print(resp)
	print("-"*15)

	conn.send(resp.encode())

	conn.close()

def get_date():
	return time.asctime(time.gmtime(time.time()))
sock = socket.socket()

try:
    sock.bind(('', PORT))
    print("Using port 80")
except OSError:
    sock.bind(('', 8080))
    print("Using port 8080")

sock.listen(5)

serv_log = logging.getLogger('log_')
serv_log_handler = logging.FileHandler('log.log', encoding = 'UTF-8')
serv_log_handler.setLevel(logging.INFO)
serv_log.addHandler(serv_log_handler)
serv_log.setLevel(logging.INFO)

while True:
	conn, addr = sock.accept()
	threading.Thread(target = process, args = [conn,addr]).start()

