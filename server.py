import socket, os

sock = socket.socket()

try:
    sock.bind(('', 80))
    print("Using port 80")
except OSError:
    sock.bind(('', 8080))
    print("Using port 8080")

sock.listen(5)

workdir = os.getcwd()
workdir = os.path.join(workdir,'www')

header = 'HTTP/1.1 200 OK\nServer: StepIgorWebServer v1.0.0\nContent-type: text/html; charset:utf-8\nConnection: close\n\n'
error404header = 'HTTP/1.1 404 Not Found\nServer: StepIgorWebServer v1.0.0'
error403header = 'HTTP/1.1 403 Forbidden\nServer: StepIgorWebServer v1.0.0'

while True:

	conn, addr = sock.accept()

	data = conn.recv(8192)
	msg = data.decode()

	print(msg)
	
	askfile = msg.split('\n')[0].split(' ')[1]
	ansfile = ''
	
	#work with FS
	
	if (askfile == '/'):
		with open(os.path.join(workdir,'index.html'),'r', encoding='UTF-8') as f:
			ansfile = f.read()
		answer = header + ansfile
		conn.send(answer.encode())
	else:
		askfile = askfile[1:len(askfile)]
		if os.path.exists(os.path.join(workdir,askfile)):
			if os.path.isfile(os.path.join(workdir,askfile)):
				with open(os.path.join(workdir,os.path.join(workdir,askfile)),'r', encoding='UTF-8') as f:
					ansfile = f.read()
				answer = header + ansfile
				conn.send(answer.encode())
			else:
				answer = error403header
				conn.send(answer.encode())
		else:
			answer = error404header
			conn.send(answer.encode())
	

	#end

	conn.close()