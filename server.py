# -*- coding: utf-8 -*-
"""
Created on Sat Nov 23 10:45:46 2019

@author: Влад
"""

import socket
import os
import logging

logging.basicConfig(filename='server.log', level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

sock = socket.socket()

def send(msgl_1, cur_dirname, addr):
    resp = ''
    if msgl_1 == '':    
        logging.info(f'{msgl_1} - {addr[0]} - 403 forbidden')
        cur_file = os.path.join(cur_dirname, 'index.html')
        data = ''
        with open(cur_file, 'r+') as f:
            for line in f:
                data+=line
        resp = """HTTP/1.1 200 OK
        Server: SelfMadeServer v0.0.1
        Content-type: text/html
        Connection: close
        
        {}""".format(data)
        return resp
    rash = msgl_1.split('.')
    if rash[1] not in ('html','css','js'):
        logging.info(f' {msgl_1} - {addr[0]} - 403 forbidden')
        resp = """HTTP/1.1 403 forbidden
        Server: SelfMadeServer v0.0.1
        Content-type: text/html
        Connection: close
        
        """
        return resp
    if os.path.isfile(os.path.join(cur_dirname, msgl_1)):
        logging.info(f'{msgl_1} - {addr[0]} - 200 OK')
        cur_file = os.path.join(cur_dirname, msgl_1)
        data = ''
        with open(cur_file, 'r+') as f:
            for line in f:
                data+=line
        resp = """HTTP/1.1 200 OK
        Server: SelfMadeServer v0.0.1
        Content-type: text/html
        Connection: close
        
        {}""".format(data)
        return resp

    else:
        logging.info(f'{msgl_1} - {addr[0]} - 404 NOT FOUND')
        resp = """HTTP/1.1 404 NOT FOUND
        Server: SelfMadeServer v0.0.1
        Content-type: text/html
        Connection: close
        
        """
        return resp


try:
    sock.bind(('', 80))
    print("Using port 80")
except OSError:
    sock.bind(('', 8080))
    print("Using port 8080")

sock.listen(5)


conn, addr = sock.accept()
print("Connected", addr)
print(conn)

data = conn.recv(8192)
msg = data.decode()

print(msg)

msgl = msg.split('\n')[0]
print(msgl)
msgl_1 = msgl.split(' ')[1]
msgl_1 = msgl_1.lstrip('/')

#Т
cur_dirname = os.path.join(os.getcwd(), 'documents')
        
new_resp = send(msgl_1, cur_dirname,addr)    
conn.send(new_resp.encode('utf-8'))  
conn.close()
    
    
