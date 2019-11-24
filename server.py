import socket


def get(msg):
    msg_m = msg.split()
    try:
        with open('templates/'+msg_m[1][1:], 'r') as f:
            htm = f.read()
    except:
        with open('templates/'+'index.html', 'r') as f:
            htm = f.read()
    return htm


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

    resp = """HTTP/1.1 200 OK
Server: SelfMadeServer v0.0.1
Content-type: text/html
Connection: close

"""+get(msg)

    conn.send(resp.encode())

    conn.close()
