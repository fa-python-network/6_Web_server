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

def set_server(settings_file,sep=";"):
    """В файле настроек хранятся: порт, запасной порт, директория, макс. объём запроса """
    settings=tuple()
    with open(settings_file) as f:
        setings=f.read().split(sep)
    return settings

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

port,backup_port,path,bufsize=set_settings("settings.txt")
try:
    sock.bind(('', port))
    print("Using port {}".format(port))
except OSError:
    sock.bind(('', backup_port))
    print("Using port {}".format(backup_port))

sock.listen(5)

conn, addr = sock.accept()
print("Connected", addr)

data = conn.recv(8192)
msg = data.decode()
content=""
code=int()

print(msg)
file=msg.split(" ")[1][0:]
if file=="/":
    file="index.html"
file=os.path.join(dir,file)
if not os.path.exists(file):
    code=404
else:
    if not valid_format(file):
        code=403
    else:
        code=200
        with open(file,"r") as f:
        for line in f:
            content+=line

resp=respond(file,content,code)

conn.send(resp.encode())

conn.close()