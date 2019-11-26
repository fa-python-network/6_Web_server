import socket
import datetime
import os

file=open('config.txt','r')
conf=''
for i in file:
    conf=conf+i
file.close()
conf=conf.split('\n')

port=int(conf[0][conf[0].find('=')+1:])
work_directory=conf[1][conf[1].find('=')+1:]
max_size=int(conf[2][conf[2].find('=')+1:])
if work_directory!='none':
    os.chdir(os.path.join(os.getcwd(), work_directory))

sock = socket.socket()
sock.bind(('', port))

sock.listen(5)

while True:
    
    conn, addr = sock.accept()
    print("Connected", addr)
    
    data = conn.recv(8192)
    msg = data.decode()
    
    path=msg[msg.find(' ')+2:msg.find('H')]
    
    output='no such file'
    
    if path[path.find('.'):-1] in ['.txt','.gif','.html','.css']:
        
        try:
            file=open(path,'r')
            output=''
            for i in file:
                
                output=output+i
            file.close()
        except:
             output='no such file'
    
    if output!='no such file':
        resp = """HTTP/1.1 200 OK
Server: SelfMadeServer v0.0.1
Date:{1}
Content-type: text/html
Connection: close

{0}""".format(output,datetime.datetime.now(),max_size)
        log=open('log.txt','a')
        log.write(str(datetime.datetime.now())+': '+str(addr)[2:str(addr).find(',')-1]+'-->'+path+':200'+'\n')
    else:
        
        if path!='' and path!='favicon.ico ':
            log=open('log.txt','a')
            log.write(str(datetime.datetime.now())+': '+str(addr)[2:str(addr).find(',')-1]+'-->'+path+':404,returned index.txt'+'\n')
            log.close()
        file=open('index.html','r')
        output=''
        for i in file:
            output=output+i
        file.close()
        resp = r"""HTTP/1.1 200 OK
Server: SelfMadeServer v0.0.1
Date:{1}
Content-type: text/html
Connection: close


{0}""".format(output,datetime.datetime.now(),max_size)
    
    conn.send(resp.encode())
    
    conn.close()
    
