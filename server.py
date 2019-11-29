import socket
import os


def make_response(code='200', status='OK', content_type='text/html; charset=utf-8;', body='', http_ver='HTTP/1.1', **kwargs):
    header = f'{http_ver} {code} {status}'

    header_fields = f'''Server: MashaLovesPython_beta
Content-Type: {content_type}
Connection: close'''
    for header_field, val in kwargs.items():
        header_fields += f'\n{header_field}: {val}'

    return f'''{header}
{header_fields}

{body}'''


def get_response(path):
    if path == '':
        with open(os.path.join(home_dir, 'index.html'), encoding='utf-8') as f:
            return make_response(body=f.read())

    parsed_by_dot = path.split('.')
    ext = parsed_by_dot[-1].lower() if len(parsed_by_dot) > 1 else 'html'

    if ext not in content_types:
        with open(os.path.join(home_dir, 'errors', 'unsupported_media_type.html'), encoding='utf-8') as f:
            return make_response(code='415', status='Unsupported Media Type', body=f.read())

    try:
        f = open(os.path.join(home_dir, path))
    except FileNotFoundError:
        with open(os.path.join(home_dir, 'errors', 'not_found.html'), encoding='utf-8') as f:
            return make_response(code='404', status='Not Found', body=f.read())
    except PermissionError:
        with open(os.path.join(home_dir, 'errors', 'forbidden.html'), encoding='utf-8') as f:
            return make_response(code='403', status='Forbidden', body=f.read())
    else:
        data = f.read()
        f.close()
        
        return make_response(content_type=content_types[ext], body=data)


content_types = {
    'html': 'text/html',
    'css': 'text/css',
    'js': 'text/javascript',
    'php': 'text/php',
    'json': 'application/json',
}

home_dir = os.path.join(*['home_dir', 'templates'])

sock = socket.socket()

host, port = 'localhost', 80
try:
    sock.bind((host, port))
    print(f"Based on {host}:{port}")
except OSError:
    print(f"{host}:{port} unavailable")
else:
    sock.listen(5)

    while True:
        conn, addr = sock.accept()
        print("Connected to", addr)

        try:
            msg = conn.recv(8192).decode()  # будем считать, что этого хватит, чтобы считать весь запрос
            print('Received:', msg, f'from "{addr}"', sep='\n', end='\n\n\n')

            header = msg.split('\n')[0]
            path = header.split(' ')[1].strip('/')

            new_resp = get_response(path)
        except BaseException:
            with open(os.path.join(home_dir, 'errors', 'not_found.html'), encoding='utf-8') as f:
                conn.send(make_response(code='500', status='Internal Server Error', body=f.read()).encode())
            conn.close()
        else:
            conn.send(new_resp.encode())
            conn.close()
