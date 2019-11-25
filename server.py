import socket

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
    
    
    
    ff = msg.split(' ')[1]
    f = ff[1:]
    print(f)
    
    if f == 'html1.txt':
        file = open('html1.txt', 'r')
        text = file.read()
        conn.send(text.encode())
        file.close()
    elif f == 'html2.txt':
        file = open('html2.txt', 'r')
        text = file.read()
        conn.send(text.encode())
        file.close()
    elif f == '':
        resp = """HTTP/1.1 200 OK
    Server: SelfMadeServer v0.0.1
    Content-type: text/html
    Connection: close
    
    Hello, webworld!"""
        
        conn.send(resp.encode())
        
    else:
        resp = """HTTP/1.1 404 Not found
    Server: SelfMadeServer v0.0.1
    Content-type: text/html
    Connection: close
    
    """
        
        conn.send(resp.encode())

    conn.close()