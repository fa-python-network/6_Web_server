import socket
import os

"""
pwd
ls
cat <filename>

"""
PORT = 8888
curr_dir = os.path.join(os.getcwd(), 'docs')
cur_dir = os.getcwd()
os.chdir('docs')
def process(req):
    global curr_dir
    if req == 'pwd':
        return curr_dir

    elif req == 'ls':
        return '; '.join(os.listdir(curr_dir))

    elif req[:6] == "mkdir ":
        os.mkdir(req[6:])
        return f'You created directory "{req[6:]}"'

    elif req[:6] == "rmdir ":
        os.rmdir(req[6:])
        return f'You deleted directory "{req[6:]}"'

    elif req[:3] == "cd ":
        curr_dir = os.path.join(os.getcwd(), req[3:])
        os.chdir(req[3:])
        return("You are in " + req[3:])

    elif req[:4] == "cat ":
        filename = req[4:]
    return 'wrong'

sock = socket.socket()
sock.bind(('', PORT))
sock.listen(5)

while True:
    print("Listening", PORT)

    conn, addr = sock.accept()


    request = conn.recv(1024).decode()
    print(request)

    response = process(request)
    conn.send(response.encode())
    conn.close()