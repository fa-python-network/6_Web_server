import socket

c=0
sock = socket.socket()
port = 80

# while True:
# 	try:
# 		sock.bind(('', port))
# 		print(f"Using port {port}")
# 		break
# 	except:
# 		port += 1
	

sock.bind(('', port))		


sock.listen(5)
print(f"Using port {port}")

while True:
	conn, addr = sock.accept()
	print("Connected", addr)

	data = conn.recv(8192)
	msg = data.decode()

	print(msg)

	try:
		fname = msg.split()[1][1:]
		print("filMEEEEEEEEE")
	except:
		fname = "home"
		print("HOMMEEEEEEEEE")
	print("\n\n\n\n\nAAAA"+fname+"AAAA\n\n\n\n\n")

	if fname == "home" or fname == '/' or fname == "":
		c +=1
		print("INNNNNNNNDEEEEEEEEEEEEEEEEX:", c)
		f = open("index.html", 'r')
		ans = f.read()
		f.close()
	else:
		if fname == "favicon.ico":
			continue
		
		try:	
			f = open(fname, 'r')
			ans = f.read()
			f.close()
		except:
			f = open("404_page.html", 'r')
			ans = f.read()
			f.close()

	# for i in range(len(ans)):
	# ans[i] = ans[i].strip('\n')
	# ans[i] = ans[i].strip('\t')
	#
	# print(ans)
	#
	# ans = ''.join(ans)

	conn.send(ans.encode())

	print(msg)
	conn.close()
'''resp = HTTP/1.1 200 OK\nServer: SelfMadeServer v0.0.1
Content-type: text/html\nConnection: close\n\nHello, webworld!\n'''

#conn.send(resp.encode())

