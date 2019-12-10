import socket

sock = socket.socket()

try:
    sock.bind(('', 80))
    print(80)
except OSError:
    sock.bind(('', 8071))
    print(8071)

sock.listen(5)


conn, addr = sock.accept()
resp="""HTTP/1.1 200 OK
Content-type: text/html

"""
data=conn.recv(8192)
msg=data.decode()
print(msg)
msgs=str(msg)

conn.send(resp.encode())

str2=""
for i in range(0,11):
	str2=str2+msg[i]
print("\n",str2)
if (str2=="GET /2.html"):
    f=open("2.html", 'r')
    str1=''
    for s in f:
	    str1=str1+s
    conn.send(str1.encode())
    f.close()

elif (str2=="GET /1.html"):
    f=open("1.html", 'r')
    str1=''
    for s in f:
	    str1=str1+s
    conn.send(str1.encode())
    f.close()
else:
	print("Takogo net")
#print("Connected", addr)
conn.close()
