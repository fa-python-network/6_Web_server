import os


class Settings:
    port = 9012
    directory = os.getcwd()
    request_size = 8192
    types = {'html': 'text/html; charset=UTF-8',
             'css': 'text/css',
             'js': 'text/javascript',
             'jpg': 'image/jpeg',
             'ico': 'image/vnd.microsoft.icon',
             'gif': 'image/gif',
             'jpeg': 'image/jpeg',
             'png': 'image/png'}
    name = "SelfMadeServer v0.0.666"
