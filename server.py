import socket
import datetime
import os

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
if dr != 'main':
    k = os.getcwd()
else:
    k = os.path.join(os.getcwd(), dr)


conn, addr = sock.accept()
print("Connected", addr)

data = conn.recv(vol)
msg = data.decode()

print(msg)
a = msg.split(' ')

'''проверка файла/запроса'''
a1 = a[1]
add = a1[1::]

#'''проверка конекта'''
#cnn = msg.split('\n')[2][12::]

'''дата'''
date = datetime.date.today()
log.writelines(str(date) + '\n')

'''проверка ip'''
ip = addr[0]
log.writelines(ip + '\n')

'''проверка файла'''
if add != '':
    log.writelines(add + '\n')
else:
    log.writelines('Without file\n_____\n')

if add == '' or add == 'index':
    tt = os.path.join(k, 'index.html')
    with open(tt, 'r') as f:
        s = ''
        s1 = ''
        for i in f:
            s+=i
            s1+=i.rstrip()
    ln = len(s1)
    resp = f"""HTTP/1.1 200 OK
    Server: SelfMadeServer v0.0.2
    Content-type: text/html
    Connection: close

Date: {date}
Content-type: text/html
Server: SelfMadeServer v0.0.2
Content-length: {ln}
Connection: close.\n
{s}"""

elif add == '1.html':
    tt = os.path.join(k, add)
    with open(tt, 'r') as f:
        s = ''
        for i in f:
            s+=i
    resp = """HTTP/1.1 200 OK
    Server: SelfMadeServer v0.0.2
    Content-type: text/html
    Connection: close

{}""".format(s)

elif add == '2.html':
    tt = os.path.join(k, add)
    with open(tt, 'r') as f:
        s = ''
        for i in f:
            s+=i
    resp = """HTTP/1.1 200 OK
    Server: SelfMadeServer v0.0.2
    Content-type: text/html
    Connection: close

{}""".format(s)

#elif add[:4] != 'html' or add[:3] != 'css' or add[:2] != 'js':
#    resp = """HTTP/1.1 403 Forbidden
#        Server: SelfMadeServer v0.0.2
#        Content-type: text/html
#        Connection: close"""

else:
    resp = """HTTP/1.1 404 Not Found
        Server: SelfMadeServer v0.0.2
        Content-type: text/html
        Connection: close"""

'''код ошибки'''
rar = resp[9::]
if int(rar[:3]) >= 400:
    log.writelines(rar[:3] + '\n')
log.writelines('_' * len(add) + '\n')

conn.send(resp.encode())

conn.close()
log.close()
#st.close()