import asyncio
import logging

from datetime import datetime


class HTTPTemplate(object):

    @staticmethod
    def html(template: str) -> dict:
        """
        Создает темплейт для HTML страницы

        :param template:
        :return:
        """

        return dict(site=template, type="HTML")

    @staticmethod
    def other_type(template: any, type: str) -> dict:
        """
        Создает темплйет для выбранного типа страницы

        :param template:
        :param type: HTML
        :return:
        """

        return dict(site=template, type=type)


class HTTPHandler(asyncio.Protocol):

    def __init__(self, server: 'HTTPServer'):
        self.host = None
        self.port = None
        self.transport = None
        self.method = None
        self.allowed_methods = ["GET"]
        self.url = None
        self.type = None
        self.code = None
        self.headers = None
        self.content = None
        self.body = None
        self._server = server

    def connection_made(self, transport) -> None:
        """
        Обрабатывает подключение

        :param transport:
        :return:
        """

        self.transport = transport
        self.host = self.transport.get_extra_info('peername')[0]
        self.port = self.transport.get_extra_info('peername')[1]
        logging.info(f"{self.host}:{self.port} - New request")

    def data_received(self, data) -> None:
        """
        Принимает данные подключения

        :param data:
        :return:
        """

        msg = data.decode()

        msg = self.__generate_response(msg)

        logging.info(f"{self.host}:{self.port} - Data received (code: {self.code}) {self.url}")

        self.transport.write(
            msg
        )

        logging.info(f"{self.host}:{self.port} - Data is sent")

        self.transport.close()

        logging.info(f"{self.host}:{self.port} - Close the peer socket")

    def __generate_response(self, request: str) -> bytes:
        """
        Генерирует ответ

        :param request:
        :return:
        """

        self.method, self.url = request.split(" ")[:2]

        # if find

        # Получает функцию из route для текущей ссылки и разрешенные методы
        server_response = self._server.check_route(self.url)

        # Запускает функцию из route
        try:
            if server_response:
                self.content = server_response["route"]()
        except Exception as e:
            logging.error(f"{self.host}:{self.port} - {e}")

        # Разрешенные методы
        if server_response is not None and "methods" in server_response:
            self.allowed_methods = server_response["methods"]

        return self.__generate_page().encode()

    def __generate_page(self) -> str:
        """
        Генерирует страницу и возращает ее

        :return:
        """

        self.__generate_code()
        self.__generate_body()
        self.__generate_header()

        return self.headers + "\r\n" + self.body

    def __generate_code(self) -> None:
        """
        Генерирует код ответа

        :return:
        """

        if not self.content:
            self.headers = f"HTTP/1.1 404 Not found\n"
            self.code = 404
        elif self.method not in self.allowed_methods:
            self.headers = f"HTTP/1.1 405 Method not allowed\n"
            self.code = 405
        else:
            self.headers = f"HTTP/1.1 200 OK\n"
            self.code = 200

    def __generate_body(self) -> None:
        """
        Генерирует тело ответа  и определяет тип возвращаемых данных

        :return:
        """

        if self.code == 404 or not self.content:
            self.body = "<h1>404</h1><p>Not found</p>"
            self.type = "HTML"
        elif self.code == 405:
            self.body = "<h1>405</h1><p>Method not allowed</p>"
            self.type = "HTML"
        else:
            self.body = self.content["site"]
            self.type = self.content["type"]

    def __generate_header(self) -> None:
        """
        Генерирует заголовки ответа

        :return:
        """

        self.headers += f"Server: {self._server.name}\n"
        self.headers += f"Date: {self._server.http_date(datetime.now())}\n"
        self.headers += f"Content-Length: {len(self.body)}\n"

        if self.type == "HTML":
            self.headers += f"Content-Type: text/html; charset=UTF-8\n"
        elif self.type == "JSON":
            self.headers += f"Content-Type: application/json\n"


class HTTPServer(object):
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s | %(levelname)s | %(message)s",
        handlers=[
            logging.FileHandler("server.log"),
            logging.StreamHandler(),
        ],
    )

    def __init__(self, host: str = "localhost", port: int = 9000, static: str = "./static", name: str = "Python3"):
        self.name = name
        self.static = static
        self.host = host
        self.port = port
        self.__urls = dict()
        self.__loop = asyncio.get_event_loop()
        self.__tasks = self.__loop.create_server(lambda: HTTPHandler(self), self.host, self.port)
        self.__server = self.__loop.run_until_complete(self.__tasks)

    def run(self) -> None:
        """
        Запускает сервер

        :return:
        """

        try:
            logging.info(f"Start server on {self.host}:{self.port}")
            self.__loop.run_forever()
        except KeyboardInterrupt:
            pass
        finally:
            self.__server.close()
            self.__loop.run_until_complete(self.__server.wait_closed())
            self.__loop.close()
            logging.info(f"Stop server")

    def route(self, rule, **options) -> 'function':
        """
        Декоратор для роутинга сервера

        :param rule:
        :param options:
        :return:
        """

        def decorator(f):
            self.__urls[rule] = dict(**options, **dict(route=f))
            return f

        return decorator

    def check_route(self, url) -> dict or None:
        """
        Проверяет существование url в route

        :param url:
        :return:
        """

        if url in self.__urls:
            return self.__urls[url]
        return None

    @staticmethod
    def http_date(dt: datetime) -> str:
        """
        RFC 1123 datetime (HTTP/1.1)

        :param dt:
        :return:
        """

        weekday = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][dt.weekday()]
        month = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"][dt.month - 1]
        return "%s, %02d %s %04d %02d:%02d:%02d GMT" % (weekday, dt.day, month, dt.year, dt.hour, dt.minute, dt.second)
