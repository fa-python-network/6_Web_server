import socket
import re


PAT = re.compile(r'[A-Z]{3,6}\s[\S]*\sHTTP/[0-9.]*', flags=re.MULTILINE) 

class Response:
    def __init__(self, html ):
        with open(html[1:], 'r', encoding='UTF-8') as file:
            self.html = file.read()
    
    def __str__(self):
        return f"""HTTP/1.1 200 OK
Server: SelfMadeServer v0.0.1
Content-type: text/html
Connection: close

{self.html}"""

    def __call__(self):
        return str(self)



def parse(req):
    return PAT.findall(req)[0].split(' ')[1]



sock = socket.socket()



try:
    sock.bind(('', 80))
    print("Using port 80")
except OSError:
    sock.bind(('', 8080))
    print("Using port 8080")

sock.listen(5)
while True:
    conn, addr = sock.accept()
    print("Connected", addr)

    data = conn.recv(8192)
    msg = data.decode()

    print(msg)
    html = parse(msg)

    conn.send(Response(html)().encode())

    conn.close()