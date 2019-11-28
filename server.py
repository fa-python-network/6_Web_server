import socket
import os
sock=socket.socket()
try:
    sock.bind(('',80))
    print("Using port 80")
except OSError:
    sock.bind(('',8080))
    print("Using port 8080")

sock.listen(5)
conn,addr=sock.accept()
print("Connected",addr)

data=conn.recv(8192)
msg=data.decode()

print(msg)
#обрабатываем сообщение от пользователя
spisok=msg.split(' ')
zapr=spisok[1][1:]
rash=str(zapr).split('.')[1]
print(rash)
if zapr in os.listdir():
    zapr1=zapr
else:
    if (rash=='html') or (rash=='txt') or (rash=='css') or (rash=='gif'):
        zapr1="htaccess"
    else:
        zapr1="htaccess1"
print("I read file [{0}]".format(zapr1))
#читаем  содержимое файла
f=open(zapr1)
vyvod=f.read()
f.close()
#собираем собщение
resp="""HTTP/1.1 200 OK
Server:SelfMadeServer v0.0.1

{0}""".format(vyvod)

conn.send(resp.encode())
conn.close()
