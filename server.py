import socket, os, time

sock = socket.socket()

with open('settings.ini','r') as f:
	settings = f.read()
	settings = settings.split('\n')

listenport = int(settings[1])

	
try:
    sock.bind(('', listenport))
    print(f'Using port {listenport}')
except OSError:
    print('Ошибка старта сервера. Порт занят!')

sock.listen(5)

workdir = os.getcwd()
workdir = os.path.join(workdir,settings[3])
print(f'Используется директория {settings[3]}')

header = ['HTTP/1.1',' ','2(code and word)','\nServer: StepIgorWebServer v1.0.0\nContent-type: ','4(content type)','; charset:utf-8\nConnection: close\nDate: ','6 (date)','\n\n']

while True:

	conn, addr = sock.accept()

	data = conn.recv(8192)
	msg = data.decode()

	print(msg)
	
	if (msg):
		askfile = msg.split('\n')[0].split(' ')[1]
	ansfile = ''
	
	#work with FS
	
	header[6] = time.strftime('%a, %d %b %Y %H:%M:%S GMT');
	
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
					with open(os.path.join(workdir,askfile),'r', encoding='UTF-8') as f:
						ansfile = f.read()
					header[2] = '200 OK'
					header[4] = 'text/html'
					answer = ''.join(header) + ansfile
					conn.send(answer.encode())
				elif (ext in ['gif','png','ico','jpg','jpeg']):
					with open(os.path.join(workdir,askfile),'rb') as f:
						ansfile = f.read()
						header[2] = '200 OK'
						header[4] = 'image/'+ext
						answer = ''.join(header).encode() + ansfile
						conn.send(answer)
				elif (ext == 'txt'):
					with open(os.path.join(workdir,askfile),'r', encoding='UTF-8') as f:
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