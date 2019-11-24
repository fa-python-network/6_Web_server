import logging

log_file = logging.FileHandler('myserver.log')
console_out = logging.StreamHandler()
logging.basicConfig(handlers=(log_file, console_out), format = '[%(asctime)]: %(message)s', datefmt='%m.%d.%Y %H:%M:%S' , level = logging.ERROR)

import socket
import os

with open('settings.txt', 'r+') as f:
    for line in f:
        HOST=line.split(';')[0]
        PORT=int(line.split(';')[1])
        max_size=int(line.split(';')[2])
 
my_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
my_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
my_socket.bind((HOST,PORT))
my_socket.listen(1)
 
print('Serving on port ',PORT)

max_size=1024

while True:
    connection,address = my_socket.accept()
    name=address[0]
    request = connection.recv(max_size).decode('utf-8')
    print(request)
    
    string_list = request.split('\n')[0] 
    method = string_list.split(' ')[1]
    requesting_file = method.lstrip('/')
    print('Client request: ', requesting_file)
    
    if(requesting_file == ''):
        requesting_file = 'index.html'
 
    myfile = os.path.join(os.getcwd(), requesting_file)
 
    try:
        file = open(myfile,'rb') # open file , r => read , b => byte format
        response = file.read()
        file.close()
 
        header = 'HTTP/1.1 200 OK\n'
 
        if(myfile.endswith(".jpg")):
            mimetype = 'image/jpg'
            header += 'Content-Type: '+str(mimetype)+'\n\n'
        elif(myfile.endswith(".css")):
            mimetype = 'text/css'
            header += 'Content-Type: '+str(mimetype)+'\n\n'
        elif(myfile.endswith(".html")):
            mimetype = 'text/html'
            header += 'Content-Type: '+str(mimetype)+'\n\n'
        else:
             header = 'HTTP/1.1 403 Not Forbidden\n\n'
             response = '''<html>
                             <body>
                                 <center>
                                     <h3>Error 403: Access to this resource on the server is denied!</h3>
                                     <p>Python HTTP Server</p>
                                </center>
                            </body>
                        </html>'''.encode('utf-8')
             logging.error(f'{name}, {requesting_file} raised Error 403 ')
            

 
    except Exception as e:
        header = 'HTTP/1.1 404 Not Found\n\n'
        response = '''<html>
                        <body>
                            <center>
                                <h3>Error 404: File not found</h3>
                                <p>Python HTTP Server</p>
                            </center>
                        </body>
                    </html>'''.encode('utf-8')
        logging.error(f'{name}, {requesting_file} raised Error 404')
 
    final_response = header.encode('utf-8')
    final_response += response
    connection.send(final_response)
    connection.close()

