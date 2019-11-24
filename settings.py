import os


class Settings:
    def __init__(self):
        self.port = 80  # Первый порт по умолчанию
        self.port2 = 8080  # Второй порт по умолчанию
        self.directory = os.getcwd()  # Рабочая директория
        self.request_size = 8192  # Размер запроса
        self.types = ['html', 'css', 'js', 'jpg', 'ico', 'gif', 'jpeg', 'png']  # Список возможных расширений
