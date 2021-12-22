import socket
import datetime

def printHtml(data_in):
    global HtmlVar
    try:
        path = data_in.split(' ')[1]
        print(path)
        if path == '/':
            with open('C:/Users/OMEN/PycharmProjects/Web_server/1.html', 'r') as file:
                HtmlVar = file.read()
        else:
            with open('C:/Users/OMEN/PycharmProjects/Web_server' + path, 'r') as file:
                HtmlVar = file.read()
    except IndexError:
        with open('views/dev_team.html', 'r') as file:
            HtmlVar = file.read()
    time = datetime.datetime.now()
    DataOut = f"""HTTP/1.1 200 OK
    Date: {time.strftime("%a, %d %b %Y %H:%M:%S")}
    Server: SelfMadeServer v0.0.1
    Content-Length: {len(HtmlVar)}
    Content-Type: text/html
    Connection: close
    {HtmlVar}"""
    return DataOut

def serverWork():
    sock = socket.socket()
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
    data_out = printHtml(msg)
    conn.send(data_out.encode())

if __name__ == '__main__':
    serverWork()