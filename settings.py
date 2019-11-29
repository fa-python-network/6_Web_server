import os


class Settings:
    def __init__(self):
        self.port = 80  
        self.port2 = 8080  
        self.directory = os.getcwd()  
        self.request_size = 8192  
        self.types = ['html', 'css', 'js', 'jpg', 'ico', 'gif', 'jpeg', 'png']  
