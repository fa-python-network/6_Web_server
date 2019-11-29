import socket
import os
import datetime
import bs4, requests

global image,text,application
text=[".txt",".css",".html"]
image=[".png",".jpeg"]
application=[".js"]

def valid_format(file,formats=[".jpeg",".txt",".png",".css",".html", ".js"]):
    """Проверяет, входит ли формат файла в список валидных"""
    if file_format(file) in formats:
        return True
    return False

def content_type(extension):
    """Определяет content-type """
    global text,image,application
    c = str()
    if extension in text:
        c="text/"
    elif extension in image:
        c="image/"    
    elif extension in application:
        c="application/"
    if c is not None:
        return c+extension[1:]
    return None

def file_format(file):
    """Определяет формат файла """
    return os.path.splitext(file)[1]

def is_image(file):
    global image
    if file_format(file) in image:
        return True
    return False

def is_text(file):
    global text
    if file_format(file) in text:
        return True
    return False

def read_image(file):
    with open(file,"rb") as f:
        content=f.read()
        return content
    
def read_text(file):
    content=str()
    with open(file,"r",encoding="utf-8") as f: #читает содержимое файла
        for line in f:
            content+=line 
    return content
    
def set_server(settings_file,sep=";"):
    """В файле настроек хранятся: порт, запасной порт, макс. объём запроса, директория """
    settings = list()
    with open(settings_file) as f:
        settings = f.read().split(sep)
        return (int(settings[0]),int(settings[1]),int(settings[2]),settings[3])
    
def get_ip():
    """Получает IP """
    s = requests.get('https://2ip.ua/ru/')
    b = bs4.BeautifulSoup(s.text, "html.parser")
    a = b.select(" .ipblockgradient .ip")[0].getText()
    return a.strip()

def log(log_file,file,code):
    """ Логирует дату, ip, код статуса в файл """
    global statuses
    date=datetime.datetime.now()
    ip=get_ip()
    if os.path.exists(log_file):
        mod="a"
    else:
        mod="w+"
    with open(log_file,mod) as f:
        f.write("Date: {}\nIP: {}\nFile: {}\nCode: {} {}\n\n".format(date,ip,file,code,statuses[code]))
        


def respond(file,content,code = 200):
    """Формирует ответ в соответствии с кодом """
    global statuses
    statuses={200: "OK", 403:"Forbidden",404: "Not Found"}
    http="HTTP/1.1"
    server="Self-Made Server v0.0.1"
    date = datetime.datetime.now()
    contenttype = content_type(file_format(file))
    contentlength = len(content)
    connection="close"
    response="{} {} {}\nDate: {}\nServer: {}\nContent-type: {}\nContent-length: {}\nConnection: {}\n\n{}".format(http,code,statuses[code],date,server,contenttype,
                 contentlength,connection,content)
    return response

def format_address(file,path):
    """Форматирует адрес файла """
    if path != "":
        file = os.path.join(path,file)
    if file == "/":
        file="index.html"
    if file[0] == "/":
        file = file[1:]
    return file

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

port,backup_port,bufsize,path = set_server("settings.txt")
try:
    sock.bind(('', port))
    print("Using port {}".format(port))
except OSError:
    sock.bind(('', backup_port))
    print("Using port {}".format(backup_port))

sock.listen(5)
while True: #многоразовый сервер
    conn, addr = sock.accept()
    print("Connected", addr)
    
    data = conn.recv(bufsize)
    msg = data.decode()
    content=""
    code = int()
    
    print(msg)
    file = msg.split("\n")[0].split(" ")[1]
    
    file = format_address(file,path)
    if not os.path.exists(file): # не существует файла -> ошибка 404
        code = 404
    else:
        if not valid_format(file): #недействительный формат файла -> ошибка 403
            code = 403
        else:
            code = 200
            if is_image(file):
                content=read_image(file)
            elif is_text(file):
                content=read_text(file)
    resp = respond(file,content,code)
    if is_image(file):
        conn.send(content)
    elif is_text(file): 
        conn.send(resp.encode())
    log("log.txt",file,code)

conn.close()