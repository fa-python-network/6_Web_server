import socket
from datetime import datetime

def http_format_date():
	date_str = "Date: "
	date = datetime.now()
	days = {0: "Mon", 1: "Tue", 2: "Wed", 3: "Thu", 4: "Fri", 5: "Sat", 6: "Sun"}
	months = {1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun", 7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"}
	day = days[date.weekday()]
	month = months[date.month]
	date_str+= day+", "+str(date.day)+" "+month+" "+str(date.year)

	return date_str


def response(filename, resp):
	resp+=http_format_date()+"\n\n"
	with open(filename, 'r') as file:
			for line in file.readlines():
				resp+=line
			file.close()
	return(resp)

sock = socket.socket()

try:
	sock.bind(('',80))
	print("Using port 80")
except OSError:
	sock.bind(('', 8080))
	print("Using port 8080")

sock.listen(5)
while True:
	conn, addr = sock.accept()
	print("Connected", addr)

	data = conn.recv(8192)
	msg = data.decode()
	print(msg)

	filename = msg.split()[1:2][0][1:]
	if filename == "":
		filename = 'index.html'

	resp = """HTTP/1.1 200 OK
Server: SelfMadeServer v0.0.1
Content-type: text/html
"""

	if ".css" in filename:	
		resp = """HTTP/1.1 200 OK
Server: SelfMadeServer v0.0.1
Content-type: text/css
"""

	try:
		resp = response(filename, resp)
	except:
		resp = """HTTP/1.1 404 Not Found
Server: SelfMadeServer v0.0.1
Content-type: text/html
"""
		resp = response('404.html', resp)								

	print(resp)
	conn.send(resp.encode())
	conn.close()