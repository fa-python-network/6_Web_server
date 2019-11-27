import socket
import datetime

sock = socket.socket()

try:
    sock.bind(('', 80))
    print("Using port 80")
except OSError:
    sock.bind(('', 8080))
    print("Using port 8080")

sock.listen(5)

conn, addr = sock.accept()
print("Connected", addr)

data = conn.recv(8192)
msg = data.decode()



print(msg)

name = msg.split(" ")[1][1:]

#print(name)


resp = """HTTP/1.1 200 OK
Server: SelfMadeServer v0.0.1
"""
resp+="Сегодняшняя дата: "+ str(datetime.date.today()) + "\n"
resp+="\n"

if name != "":
    try:
        with open(name, 'r', encoding='utf-8') as file:
            resp += file.read()
    except FileNotFoundError:
        with open('404.html', 'r', encoding='utf-8') as file:
            resp += file.read()

conn.send(resp.encode())

conn.close()
