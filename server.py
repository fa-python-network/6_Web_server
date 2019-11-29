import socket
import yaml
import os


def main():
    sock.listen(5)

    while True:
        conn, addr = sock.accept()

        print(f'Connected to "{addr}"')

        try:
            req = conn.recv(REQ_MAX_SIZE).decode()
            print(f'Received "{req}" from "{addr}"\n')

            header = req.split('\n')[0]
            path = header.split(' ')[1].strip('/')

            with open(os.path.join(base_dir, path if path else 'index.html')) as f:
                parsed_path = path.split('.')
                cont_type = 'text/'
                if len(parsed_path) > 1:
                    cont_type += parsed_path[-1].lower()
                else:
                    cont_type += 'html'
                cont_type += '; charset=utf-8'

                resp = f"""HTTP/1.1 200 OK
Server: ConfigurableServer
Content-Type: {cont_type}
Connection: close

{f.read()}"""
        except BaseException as err:
            conn.send("""HTTP/1.1 500 Internal Server Error
Server: ConfigurableServer
Content-Type: text/html; charset=utf-8
Connection: close

<h1>Internal Server Error</h1>""".encode())
            conn.close()
        else:
            conn.send(resp.encode())
            conn.close()


sock = socket.socket()

with open('config.yaml') as conf_file:
    config = yaml.load(conf_file, yaml.FullLoader)

print(config)
base_dir = config['base_dir']
HOST, PORT = config['host'], config['port']
REQ_MAX_SIZE = config['req_max_size']

try:
    sock.bind((HOST, PORT))
    print(f"Server started on {HOST}:{PORT}")
except OSError:
    print(f"{HOST}:{PORT} unavailable")
else:
    main()
