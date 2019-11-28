import socket
import os
import datetime

def valid_format(file,formats=["jpeg","txt","png","css","html", "js"]):
    """Проверяет, входит ли формат файла в список валидных"""
    if file_format(file) in formats:
        return True
    return False

def file_format(file):
    """Определяет формат файла """
    return os.path.splitext(file)[1]

def content_type(extension):
    """Определяет content-type """
    text=["txt","css","html"]
    image=["png","jpeg"]
    application=["js"]
    if extension in text:
        return "text/"+extension
    if extension in image:
        return "image/"+extension
    if extension in application:
        return "application/"+extension


def respond(file,content,code=200):
    """Формирует ответ в соответствии с кодом """
    statuses={200: "OK", 403:"Forbidden",404: "Not Found"}
    http="HTTP/1.1"
    server="Self-Made Server v0.0.1"
    date=datetime.datetime.now()
    content_type=content_type(file_format(file))
    content_length=len(content)
    connection="close"
    response="{} {} {}\nDate: {}\nServer: {}\nContent-type: {}\nContent-length: {}\n \
    Connection: {}".format(http,code,statuses[code],date,server,content_type,
                 content_length,connection)
    return response

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
content=""
code=int()

print(msg)
link=msg.split(" ")[1][0:]
if link=="/":
    link="index.html"
print(link)
if not os.path.exists(link):
    code=404
else:
    if not valid_format(link):
        code=403
    else:
        code=200
        with open(link,"r") as f:
        for line in f:
            content+=line

resp=respond(link,content,code)

conn.send(resp.encode())

conn.close()