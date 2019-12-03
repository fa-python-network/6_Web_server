# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 08:48:18 2019

@author: 187056
"""
import socket
sock = socket.socket()
try:
    sock.bind(('',80))
except OSError:
    sock.bind(('',8080))
sock.listen(5)

conn, addr = sock.accept()
print("Connected", addr)


# Чтение файла     
#file = open("index.txt","r")
#rd = file.read()
#file.close()

data = conn.recv(8192)
msg = data.decode()

print(msg)

lst = msg.split(' ')
name_file = lst[1][1:]

# Чтение файла     
file = open(name_file)
rd = file.read()
file.close()

# Для вывода данных из файла 
resp = """HTTP/1.1 200 OK

{0}""".format(rd)

conn.send(resp.encode())
conn.close()
