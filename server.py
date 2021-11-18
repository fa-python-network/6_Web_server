import socket
import datetime

sock = socket.socket()

try:
    sock.bind(('', 83))
    print("Используем порт 83")
except OSError:
    sock.bind(('', 8080))
    print("Используем порт 8080")

sock.listen(5)

conn, addr = sock.accept()
print("Подключено", addr)

data = conn.recv(8192)
msg = data.decode()

print(msg)


nowdate = datetime.datetime.utcnow().strftime(r"%a, %d %b %Y %H:%M:%S GMT")
print(nowdate)
content = "Hello world!"
content_length = len(content)
resp = f"""HTTP/1.1 200 OK
Date: {nowdate}
Content-length: {content_length}
Server: SelfMadeServer v0.0.1
Content-type: text/html; charset = utf8
Connection: close

{content}"""

conn.send(resp.encode())

conn.close()