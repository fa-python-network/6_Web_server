import socket
import os

sock = socket.socket()

port = 80
while port != 65536:
    try:
        sock.bind(('', port))
        break
    except:
        port += 1

print('Port: ', port)
sock.listen(5)

conn, addr = sock.accept()
print("Connected", addr)

data = conn.recv(8192)
msg = data.decode()

msg1 = msg.split(' ')[1]
print(msg1[1:])
print(os.path.abspath('index.html'))

if msg1 == '/':
    file = open('index.html', 'r')
    content = file.read()
    conn.send(content.encode())
    file.close()
elif os.path.exists(os.path.abspath(str(msg1[1:]))) == True:
    file = open(str(msg1[1:]), 'r')
    content = file.read()
    conn.send(content.encode())
    file.close()
else:
    resp1 = """HTTP/1.1 404 NOT FOUND
    Server: SelfMadeServer v0.0.1
    Content-type: text/html
    Connection: close
    """
    conn.send(resp1.encode())

conn.close()
