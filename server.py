import socket
import magic
from datetime import datetime

sock = socket.socket()

def locate(dec_inf, conn):
    result=dec_inf.split('\n')[0].split()[1][1:] #вытаскиваем из запроса имя страницы
    currentDate = datetime.now().strftime("%a, %d %b %Y %H:%M:%S GTM")
    content_type = "text/html; charset=utf-8"
    if not result:
        result = "index.html"
    try:
        if result.split('.')[1] == ("jpeg", "jpg"):
            mime = magic.Magic(mime=True)
            content_type = mime.from_file(f"./{result}")
    except:
        pass
    send_this=f'''HTTP/1.1 200 OK
    Server: SelfMadeServer v0.0.1
    Date: {currentDate}
    Content-Type: {content_type}
    Connection: close\n\n'''

    send_if_error=f'''HTTP/1.1 400 ERROR 
    Server:SelfMadeServer v0.0.1
    Date: {currentDate}
    Content-Type: multipart/form-data; charset=utf-8
    Connection: close \n\n'''
    try:
        with open(result,'rb') as file:
            info=file.read()
            to_encode=send_this.encode()+info
            conn.send(to_encode)
    except FileNotFoundError:
        with open('404.html','rb') as err:
            info=err.read()
            to_encode=send_if_error.encode()+info
            conn.send(to_encode)


def manipulator(conn):
    inf=conn.recv(8192) # получаем запрос по 8кб
    dec_inf=inf.decode() #переводим из битового представления
    locate(dec_inf, conn)

def server_starter():
    try:
        sock.bind(('', 80))
        print("Using port 80")
    except OSError:
        sock.bind(('', 8080))
        print("Using port 8080")

    sock.listen(5)
    while True:
        try:
            conn, addr = sock.accept()
            print("Connected", addr)
            manipulator(conn)

        except KeyboardInterrupt:
            conn.close()
            break

if __name__=='__main__':
    server_starter()
