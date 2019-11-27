import socket
import os

def read_file(name):
    content = ''
    testFile = open(name,'r', encoding='utf-8')
    #Самая бесполезная вещь за сегодняшний день(кроме сема по экселю)
    # зачем-то написала этот кусок кода, который ищет полный путь к картинке
    for line in testFile:
        if line.find('<img')!= -1:
            z = line.split('"')
            z[1] = os.path.join(os.getcwd(), z[1])
            line = ''
            for i in z:
                line += i + '"'
            line = line[0:-1]
            print(line)

        content += line
    testFile.close()
    return content

sock = socket.socket()

try:
    sock.bind(('', 80))
    print("Using port 80")
except OSError:
    sock.bind(('', 8080))
    print("Using port 8080")

#sock.listen(5)
while True:
    sock.listen(5)
    conn, addr = sock.accept()
    print("Connected", addr)

    data = conn.recv(8192)
    msg = data.decode()
    print(msg)
    try:
        x = msg.split('\n')[0].split(' ')[1]
        print(x)
        print(os.getcwd())
        if os.path.exists(os.path.join(os.getcwd(), x[1:])):
            x = read_file(x[1:])

        resp = f""""HTTP/1.1 200 OK
Server: SelfMadeServer v0.0.1
Content-type: text/html
Connection: close
Charset: utf-8

{x}"""
    except IndexError:
        pass
    conn.send(resp.encode())
    conn.close()
