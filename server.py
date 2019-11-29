import socket, os, time #сокеты, получение путей и размера файлов, время для полей и логов

sock = socket.socket()

with open('settings.ini','r') as f:		#файо с настройками сервера
	settings = f.read()
	settings = settings.split('\n')

listenport = int(settings[1])		#прослушиваемый порт

	
try:								#проверяем, свободен ли порт
    sock.bind(('', listenport))
    print(f'Using port {listenport}')
except OSError:
    print('Ошибка старта сервера. Порт занят!')

sock.listen(5)

workdir = os.getcwd()
workdir = os.path.join(workdir,settings[3])		#текущая директория с учетом параметра в файле настроек
print(f'Используется директория {settings[3]}')

#универсальный заголовок, поддерживаемый путем изменения значений по индексу, выводится join
header = ['HTTP/1.1',' ','2(code and word)','\nServer: StepIgorWebServer v1.0.0\nContent-type: ','4(content type)','; charset:utf-8\nConnection: close\nDate: ','6 (date)','\n\n']

while True:

	conn, addr = sock.accept()

	data = conn.recv(8192)
	msg = data.decode()

	print(msg)		#вывод заголовка в консоль (от клиента)
	
	if (msg):
		askfile = msg.split('\n')[0].split(' ')[1]
	ansfile = ''
	
	#work with FS
	#дата запроса
	header[6] = time.strftime('%a, %d %b %Y %H:%M:%S GMT');
	
	with open('access.log','a') as f:	#запись в лог
		f.write(f'{header[6]} - {addr} - {askfile} - ')
	
	if (askfile == '/'):	#если просят корень
		with open(os.path.join(workdir,'index.html'),'r', encoding='UTF-8') as f:
			ansfile = f.read()
			
		header[2] = '200 OK'
		header[4] = 'text/html'
		answer = ''.join(header) + ansfile	#заголовок + тело
		conn.send(answer.encode())
	else:
		askfile = askfile[1:len(askfile)]
		
		try:
			if (askfile.split('.')[1]):			#попытка получить расширение запрашиваемого файла
				ext = askfile.split('.')[1]
		except:
			ext = 'none'
			
		if os.path.exists(os.path.join(workdir,askfile)):		#если файл существует (путь)
			if os.path.isfile(os.path.join(workdir,askfile)):		#если это файл (иначе кидаем 403)
				if ext == 'html':									#далее сравнения по расширениям
					with open(os.path.join(workdir,askfile),'r', encoding='UTF-8') as f:
						ansfile = f.read()
					header[2] = '200 OK'
					header[4] = 'text/html'
					answer = ''.join(header) + ansfile
					conn.send(answer.encode())
					with open('access.log','a') as f:		#дополнить лог кодом ответа
						f.write(f'{header[2]}\n')
				elif (ext in ['gif','png','ico','jpg','jpeg']):
					with open(os.path.join(workdir,askfile),'rb') as f:
						ansfile = f.read()
					header[2] = '200 OK'
					header[4] = 'image/'+ext
					answer = ''.join(header).encode() + ansfile
					conn.send(answer)
					with open('access.log','a') as f:
						f.write(f'{header[2]}\n')
				elif (ext == 'txt'):
					with open(os.path.join(workdir,askfile),'r', encoding='UTF-8') as f:
						ansfile = f.read()
					header[2] = '200 OK'
					header[4] = 'text/txt'
					answer = ''.join(header) + ansfile
					conn.send(answer.encode())
					with open('access.log','a') as f:
						f.write(f'{header[2]}\n')
				else:		#если запрещенный тип файла
					header[2] = '403 Forbidden'
					header[4] = 'text/html'
					answer = ''.join(header)
					conn.send(answer.encode())
					with open('access.log','a') as f:
						f.write(f'{header[2]}\n')
			else:		#если хотят открыть директорию
				header[2] = '403 Forbidden'
				header[4] = 'text/html'
				answer = ''.join(header)
				conn.send(answer.encode())
				with open('access.log','a') as f:
						f.write(f'{header[2]}\n')
		else:		#если путь не найден
			header[2] = '404 Not Found'
			header[4] = 'text/html'
			answer = ''.join(header)
			conn.send(answer.encode())
			with open('access.log','a') as f:
						f.write(f'{header[2]}\n')
	

	#end

	conn.close()