import socket
#import datetime
import os
import time

log = open('log.txt', 'a+')
st = open('settings.txt').readlines()
port = 0
dr = os.getcwd()
vol = 0

for i in iter(st):
    if "port" in i:
        port = int(i[5::])
    if "dir" in i:
        dr = i[4::]
    if "vol" in i:
        vol = int(i[4::])

sock = socket.socket()

try:
    sock.bind(('', 80))
    print("Using port 80")
except OSError:
    sock.bind(('', port))
    print("Using port " + str(port))

sock.listen(5)

k = ''
try:
    if dr.rstrip() == 'main':
        k = os.getcwd()
    else:
        k = os.path.join(os.getcwd(), dr.rstrip())
except:
    k = os.path.join(os.getcwd(), dr.rstrip())

conn, addr = sock.accept()
print("Connected", addr)

data = conn.recv(vol)
msg = data.decode()

print(msg)
a = msg.split(' ')

'''проверка файла/запроса'''
a1 = a[1]
add = a1[1::]
try:
    pnt = add.split('.')
    pnt = pnt[1].rstrip()
except:
    pnt = ''

#'''проверка конекта'''
#cnn = msg.split('\n')[2][12::]

'''дата'''
tm = time.time()
tm = str(time.ctime(tm))
log.writelines(tm + '\n')
#date = datetime.date.today()
#log.writelines(str(date) + '\n')

'''проверка ip'''
ip = addr[0]
log.writelines(ip + '\n')

'''проверка файла'''
if add != '':
    log.writelines(add + '\n')
else:
    log.writelines('Without file\n_____\n')

try:
    if add.rstrip() == '':
        tt = os.path.join(k, 'index.html')
        tt = tt.replace('\\','/')
        with open(tt, 'r', encoding='utf-8') as f: 
            s = ''
            s1 = ''
            for i in f:
                s1 += i
                s += i
            s1 = len(s1)
        resp = f"""HTTP/1.1 200 OK
        {tm}
        Server: SelfMadeServer v0.0.2
        Content-type: text/html
        {s1}
        Connection: close


{s}"""

    elif  pnt != 'html' and pnt != 'js' and pnt != 'css':
        resp = f"""HTTP/1.1 403 Forbidden
        Server: SelfMadeServer v0.0.2
        Content-type: text/html
        Connection: close"""
        
    else:
        tt = os.path.join(k, add)
        with open(tt, 'r', encoding='utf-8') as f:
            s = ''
            s1 = ''
            for i in f:
                s1 += i
                s += i
            s1 = len(s1)
        resp = f"""HTTP/1.1 200 OK
        {tm}
        Server: SelfMadeServer v0.0.2
        Content-type: text/html
        {s1}
        Connection: close

{s}"""
    
except FileNotFoundError:
    resp = f"""HTTP/1.1 404 Not Found
        {tm}
        Server: SelfMadeServer v0.0.2
        Content-type: text/html
        {s1}
        Connection: close"""

'''код ошибки'''
rar = resp[9::]
if int(rar[:3]) >= 400:
    log.writelines(rar[:3] + '\n')
log.writelines('_' * 5 + '\n')

conn.send(resp.encode())

conn.close()
log.close()
#st.close()