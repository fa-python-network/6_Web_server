import socket
import re
import datetime

HOST = '127.0.0.1'
PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()

    #while True:
    conn, addr = s.accept()

    with conn:
        print(f'Connected by {addr}')

        data = conn.recv(8192).decode()
        print(data)

        request = ''
        if match := re.search(r'GET /(?P<requested_entity>.+) HTTP/1.1', data):
            request = match.group(1)
        
        print(f'Request: /{request}')

        if re.match(r'.+\.(txt|html|css|js)', request):
            response = f"""HTTP/1.x 200 OK
Content-Type: text/html; charset=UTF-8
Date: {datetime.date.today()}
Connection: close

"""
            try:
                with open(f'content/{request}') as f:
                    response += f.read()
            except:
                with open('content/index.html') as f:
                    response += f.read()
        else:
            response = f'HTTP/1.x 403 Forbidden\nDate: {datetime.date.today()}\nConnection: close'

        conn.sendall(response.encode())
