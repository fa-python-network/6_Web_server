import socket
 
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
name = msg.split()[1][1:]
if name == "": name = "HTML1.html"
 
print(name)
 
resp = """HTTP/1.1 200 OK
Server:SelfMadeServer v0.0.1
 
"""
try:
    with open(name, "r", encoding="utf-8") as file:
        resp += file.read()
except FileNotFoundError:
    resp += """<html>
<head>
<meta charset="utf-8">
</head>
<body>
<h1>Здрасте</h1>
<h2>Всё тута(</h2>
</body>
</html>"""
 
 
conn.send(resp.encode())
 
 
conn.close()