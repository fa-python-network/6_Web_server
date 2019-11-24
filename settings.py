import os


class Settings:
    def __init__(self):
        self.port = 9090  # Первый порт по умолчанию
        self.port2 = 8080  # Второй порт по умолчанию
        self.directory = os.getcwd()  # Рабочая директория
        self.request_size = 8192  # Размер запроса
        self.types = ['html', 'css', 'js', 'jpg']  # Список возможных расширений
        self.pictures = ['jpg']  # Список расширений картинок (оба этих списка, естественно, стоит дополнить,
        # но для лабы в этом нет необходимости)
