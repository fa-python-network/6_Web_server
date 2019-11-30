# -*- coding: utf-8 -*-
import socket, re, datetime, os, logging
from threading import Thread

logging.basicConfig(filename="serv.log", level=logging.INFO)
allowed_types = ['.html', '.css', '.js', '.txt']
now = datetime.datetime.now()

#===========================================================

def serv(conn, addr):
    
    print("Connection", addr)
    
    data = conn.recv(8192)
    msg = data.decode()
    
    print(msg)
    
    fl = re.search(r'/.* ', msg)
    
    code = 200
    
    try:
        if "/ " in fl.group():
            fl = os.getcwd() + '/index.html'
            flrq = "index.html"
            
            try:
                with open (fl, "r") as f:
                    flshow = f.read()
                    
            except:
                code = 404
                
        else:
            flrq = fl.group()[1:-1]
            fl = os.getcwd() + fl.group()[:-1]   
            
            try:
                flch = re.search(r'[.].*', flrq)
                flch = flch.group()
                
                if flch not in allowed_types:
                    code = 403
                    
                else:
                    try:
                        with open (fl, "r") as f:
                            flshow = f.read()
                            
                    except:
                        code = 404
                        
            except:
                code = 403
                
    except:
        return
            
    


    if code == 200:
        resp = f"""HTTP/1.1 200 OK
Date: {now}
Server: SelfMadeServer v0.0.1
Content-type: text/html
Connection: close

{flshow}
"""
    elif code == 404:
        resp = f"""HTTP/1.1 404 Not Found
Date: {now}
Server: SelfMadeServer v0.0.1
Content-type: text/html
Connection: close

<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
<html>
<head>
<title>404 Not Found</title>
</head>
<body>
<h1>Not Found</h1>
<p>The requested URL was not found on this server.</p>
</body>
</html>
"""
    elif code == 403:
        resp = f"""HTTP/1.1 403 Forbidden
Date: {now}
Server: SelfMadeServer v0.0.1
Content-type: text/html
Connection: close

<!DOCTYPE html>
<html lang="en"><head>
<title>403 Forbidden</title>
</head><body>
<h1>Forbidden</h1>
<p>You don't have permission to access /.htaacces
on this server.</p>
</body></html>
"""
        
    logging.info(f"{now}. {addr}, {flrq}, {code}")
    conn.send(resp.encode())
    conn.close()

#===========================================================

sock = socket.socket()

try:
    sock.bind(('', 80))
    print("Using port 80")
    
except:
    sock.bind(('', 8080))
    print("Using port 8080")
    
sock.listen(1)

while True:
    
    conn, addr = sock.accept()
    Thread(target=serv, args=(conn, addr)).start()