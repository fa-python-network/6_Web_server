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

header = ['HTTP/1.1',' ','2(code and word)','\nServer: StepIgorWebServer v1.0.0\nContent-type: ','4(content type)','; charset:utf-8\nConnection: close\n\n']

while True:

	conn, addr = sock.accept()

	data = conn.recv(8192)
	msg = data.decode()

	print(msg)
	
	if (msg):
		askfile = msg.split('\n')[0].split(' ')[1]
	ansfile = ''
	
	#work with FS
	
	if (askfile == '/'):
		with open(os.path.join(workdir,'index.html'),'r', encoding='UTF-8') as f:
			ansfile = f.read()
		header[2] = '200 OK'
		header[4] = 'text/html'
		answer = ''.join(header) + ansfile
		conn.send(answer.encode())
	else:
		askfile = askfile[1:len(askfile)]
		
		try:
			if (askfile.split('.')[1]):
				ext = askfile.split('.')[1]
		except:
			ext = 'none'
			
		if os.path.exists(os.path.join(workdir,askfile)):
			if os.path.isfile(os.path.join(workdir,askfile)):
				if ext == 'html':
					with open(os.path.join(workdir,os.path.join(workdir,askfile)),'r', encoding='UTF-8') as f:
						ansfile = f.read()
					header[2] = '200 OK'
					header[4] = 'text/html'
					answer = ''.join(header) + ansfile
					conn.send(answer.encode())
				elif (ext in ['gif','png','ico','jpg','jpeg']):
					with open(os.path.join(workdir,os.path.join(workdir,askfile)),'rb') as f:
						ansfile = f.read()
						header[2] = '200 OK'
						header[4] = 'image/'+ext
						answer = ''.join(header).encode() + ansfile
						conn.send(answer)
				elif (ext == 'txt'):
					with open(os.path.join(workdir,os.path.join(workdir,askfile)),'r', encoding='UTF-8') as f:
						ansfile = f.read()
					header[2] = '200 OK'
					header[4] = 'text/txt'
					answer = ''.join(header) + ansfile
					conn.send(answer.encode())
				else:
					header[2] = '200 OK'
					header[4] = 'text/html'
					answer = ''.join(header) + 'Сервер не умеет отдавать файлы такого формата :('
					conn.send(answer.encode())
			else:
				header[2] = '403 Forbidden'
				header[4] = 'text/html'
				answer = ''.join(header)
				conn.send(answer.encode())
		else:
			header[2] = '404 Not Found'
			header[4] = 'text/html'
			answer = ''.join(header)
			conn.send(answer.encode())
	

	#end

	conn.close()