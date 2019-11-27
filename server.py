from threading import Thread
from socket import socket, AF_INET, SOCK_STREAM
import exceptions as e
from collections import namedtuple
from os import getcwd, path
from time import asctime

DEFAULT_HEADERS = {'Connection': 'close'}  # Я ожидал, что их будет больше

CONTENT_TYPES = {
    '.jpg': 'image/jpeg',
    '.png': 'image/png',
    '.gif': 'image/gif',
    '.html': 'text/html',
    '.json': 'application/json'
}


class Request:
    def __init__(self, method, target, proto, headers, file):
        self.method = method
        self.target = target
        self.proto = proto
        self.headers = headers
        self.file = file


class Response:
    def __init__(self, status, reason, headers=None, body=None):
        self.status = status
        self.reason = reason
        self.headers = headers
        self.body = body



class HTTPServer:
    def __init__(self, host: str, port: int, server_name: str = 'Default HTTP server'):
        self.__host = host
        self.__port = port
        self.__server_name = server_name
        self.__path = getcwd()

    def serve_forever(self):
        self.sock = socket(AF_INET, SOCK_STREAM)

        try:
            self.sock.bind((self.__host, self.__port))
            self.sock.listen()
            print('Serving...')
            while True:
                conn, addr = self.sock.accept()
                print(f'Connected {addr}')
                # Каждого клиента направляем в отдельный поток
                Thread(target=self.handle_client, args=(conn,)).start()
        finally:
            self.sock.close()

    def handle_client(self, conn: socket):
        try:
            while True:
                # Парсим реквест
                req = self.parse_request(conn)
                print(req.method, req.target, req.proto)
                # Создаем для него нормальный респонз
                resp = self.handle_request(req)
                # И шлем его клиенту
                self.send_response(conn, resp)
        except Exception as e:
            print(f'{e.__class__.__name__}: {e}')
        finally:
            conn.close()

    def parse_request(self, conn: socket) -> Request:
        # Все чтение сокета делал через файлы, так удобнее читать построчно
        file = conn.makefile('rb')
        data = file.readline(1024*64)

        # Нагуглил, что хедеры обязаны быть в этой кодировке
        line = data.decode('iso-8859-1')
        line = line.strip().split()
        if len(line) != 3:  # Ожидаем метод, цель и протокол
            raise e.BadRequest('Request first line have to be 3 parts')
        method, target, proto = line

        # Перенаправляем / на /index.html
        if target == '/':
            target = '/index.html'

        # Других скорее всего и не будет, но на всякий
        if proto != 'HTTP/1.1':
            raise e.UnexpectedProto('Unexpected HTTP version')

        headers = self.parse_headers(file)
        host = headers.get('Host')
        if not host or host.strip() not in [self.__host, f'{self.__host}:{self.__port}']:
            raise e.BadRequest('Not found')
        return Request(method, target, proto, headers, file)

    def parse_headers(self, file) -> dict:
        """
        Читаем и сплитим строку, пока не встретим пустую, 
        полученные строки кидаем в словарь
        """
        headers = {}
        while True:
            line = file.readline()

            if line in [b'\r\n', b'\n', b'']:
                return headers
            line = line.decode('iso-8859-1')
            k, v = line.strip('\r\n').split(':', 1)
            headers[k] = v


    def handle_request(self, req):
        not_found = False
        # Путь к искомому файлу записывается как `/файл`, из-за этого os.path.join
        # некорректно отрабатывает, приходится отрубать ему передний слеш
        path_ = path.join(self.__path, req.target[1:])
        if not path.exists(path_):
            # Файла нет - получаем 404
            path_ = path.join(self.__path, '404.html')
            not_found = True
        with open(path.join(path_), 'rb') as f:
            data = f.read()
        for k, v in CONTENT_TYPES.items():
            if req.target.endswith(k):
                content_type = v
                break
        else:
            content_type = 'text/html'
        return Response(404 if not_found else 200, 'Not found' if not_found else 'OK', {**DEFAULT_HEADERS, 'Date': asctime(), 'Content-length': len(data), 'Server': self.__host, 'Content-type': content_type}, data)

    def send_response(self, conn: socket, resp):
        # Опять же пишем в файл
        file = conn.makefile('wb')
        # Записываем первую строку
        file.write(f'HTTP/1.1 {resp.status} {resp.reason}\r\n'.encode('iso-8859-1'))

        # Все хедеры
        if resp.headers:
            for k, v in resp.headers.items():
                file.write(f'{k}: {v}\r\n'.encode('iso-8859-1'))

        # и разделитель
        file.write(b'\r\n')

        if resp.body:
            file.write(resp.body)
        file.flush()
        file.close()

    def send_error(self, conn: socket, err):
        pass  # TODO: implement me!


if __name__ == "__main__":
    host = input('Host (optional):') or 'localhost'
    port = input('Port (optional): ') or 80
    port = int(port)
    name = input('Server name (optional): ')
    server = HTTPServer(host, port, name)
    try:
        server.serve_forever()
    finally:
        print('Goodbye!')
