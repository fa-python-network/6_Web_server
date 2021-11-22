import socket
import datetime

def serv_setts():
    sock = socket.socket()
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
      sock.bind(('', 80))
    except OSError:
      sock.bind(('', 8080))
    sock.listen(5)

    conn, addr = sock.accept()
    print("Connected", addr)
    data = conn.recv(8192)
    msg = data.decode()
    print(msg)
    content = repres_web(msg)
    conn.send(content.encode())

now = datetime.datetime.now()

def repres_web(request_data):
    global response
    HDRS = "HTTP/1.1 200 OK"
    try:
        path = request_data.split(' ')[1]
        print(path)
        response = ''
        if path == '/':
            with open('views/dev_team.html','r') as file:
                response = file.read()
        else:
            with open('views' + path,'r') as file:
                response = file.read()

    except IndexError:
        with open('views/dev_team.html', 'r') as file:
            response = file.read()

    HDRS = f"""HTTP/1.1 200 OK
Date: {now.strftime("%a, %d %b %Y %H:%M:%S")}
Server: SelfMadeServer v0.0.1
Content-Length: {len(response)}
Content-Type: text/html
Connection: close

{response}"""

    return HDRS




if __name__ == '__main__':
    serv_setts()