import socket
import os
import datetime

def read_file(name):
    content = ''
    file = open(name, 'r', encoding='utf-8')
    for line in file:
        if line.find('<img')!= -1:
            z = line.split('"')
            z[1] = os.path.join('http://localhost:8080', z[1])
            line = ''
            for i in z:
                line += i + '"'
            line = line[0:-1]
            print(line)
        content += line
    file.close()
    return content.encode()

def read_img(name):
    f = open(name, 'rb')
    c = f.read()
    f.close()
    return c

sock = socket.socket()



try:

    sock.bind(('', 80))

    #print("Using port 80")

except OSError:

    sock.bind(('', 8080))

    #print("Using port 8080")






while True:
    sock.listen(5)
    conn, addr = sock.accept()

    #print("Connected", addr)



    data = conn.recv(8192)

    msg = data.decode()
   
    print(msg)
    try:
        x = msg.split('/n')[0].split(' ')[1]
        p = os.path.exists(os.path.join(os.getcwd(), x[1:]))
        type = 'text/html'
        print(x)
        now = datetime.datetime.now()
        status_code = '200 OK'
        if p and x.split('.')[-1] == 'html':
            x = read_file(x[1:])
            type = 'text/html'
        elif p and x.split('.')[-1] == 'jpg':
            x = read_img(x[1:])
            type = 'image/jpeg'
        elif p and x.split('.')[-1] == 'png':
            x = read_img(x[1:])
            type = 'image/png'
        elif p and x.split('.')[-1] == 'gif':
            x = read_img(x[1:])
            type = 'image/gif'
        elif not p:
            status_code = '404'
            #x = read_file('404.html')
            type = 'text/html'
            x = x.encode()
        elif p:
            status_code = '403'
            #x = read_file('403.html')
            type = 'text/html'
            x = x.encode()
        else:
            x = x.encode()
        
    


        resp = f"""HTTP/1.1 {status_code}
Server: SelfMadeServer v0.0.1
Content-type: {type}
Content-length: {len(x)}
Data: {now}
Connection: close
Charset: utf-8

"""
    except IndexError:
        pass

    conn.send(resp.encode()+x)
    conn.close()