import socket
from threading import Thread
import os


def main():
    def process_client(conn, addr):
        print(f'Connected to "{addr}"')

        try:
            msg = conn.recv(8192).decode()
            print(f'Received "{msg}" from "{addr}"\n')

            header = msg.split('\n')[0]
            path = header.split(' ')[1].strip('/')

            with open(os.path.join(work_dir, path if path else 'index.html')) as f:
                parsed_path = path.split('.')
                cont_type = 'text/' + parsed_path[-1].lower() if len(parsed_path) > 1 else 'html' + '; charset=utf-8'

                resp = f"""HTTP/1.1 200 OK
Server: MyBestServer
Content-Type: {cont_type}
Connection: close

{f.read()}"""
        except BaseException as err:
            print(err)
            conn.send("""HTTP/1.1 500 Internal Server Error
Server: MyBestServer
Content-Type: text/html; charset=utf-8
Connection: close

<h1>Внутренняя ошибка сервера</h1>""".encode())
            conn.close()
        else:
            conn.send(resp.encode())
            conn.close()

    sock.listen(5)

    while True:
        Thread(target=process_client, args=sock.accept()).start()


work_dir = os.path.join(*['work_dir', 'templates'])

sock = socket.socket()

host, port = 'localhost', 80
try:
    sock.bind((host, port))
    print(f"Based on {host}:{port}")
except OSError:
    print(f"{host}:{port} unavailable")
else:
    main()
