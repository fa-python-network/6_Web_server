import os


class Settings:
    def __init__(self):
        self.port = 80  # Первый порт по умолчанию
        self.port2 = 8080  # Второй порт по умолчанию
        self.directory = os.getcwd()  # Рабочая директория
        self.request_size = 8192  # Размер запроса
        self.dict = {'html': "text/html; charset=utf-8", 'css': "text/css; charset=utf-8",
                     'js': "text/javascript; charset=utf-8", 'jpeg': "image/jpeg", 'gif':"image/gif", 'png':"image/png",
                     "ico":"vnd.microsoft.icon"}
