import socket
import os
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
n = msg.split()[1][1:]
rasr = str(n).split('.')[1]
print(n)
print('--------------------')
print(rasr)
dost_rasr = ["js","html","css","php","jpg", "png", "gif", "ico"]
if n in os.listdir():
    file = n
elif rasr in dost_rasr:
    file = "404.html"
else:
    file = "403.html"
    
res = open(file)
result = res.read()
print("\nFile:\n", result)

resp = """HTTP/1.1 200 OK
Server: SelfMadeServer v0.0.1
        
{0}""".format(result)

    
conn.send(resp.encode())
    
conn.close()