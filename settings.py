class GeneralSettings:
    HOST = "127.0.0.1"
    PORT = 8080
    ALTER_PORT = 9090
    ENCODING = "UTF-8"
    BUFFER_SIZE = 1024 * 8
    MIN_PORT = 8000
    MAX_PORT = 9000


class CipherSettings:
    MAX_ORD = 2 ** 16 - 1


class PathsStorage:
    CLIENT_PUBLIC_KEY = "keys\\public_client_key.txt"
    CLIENT_PRIVATE_KEY = "keys\\private_client_key.txt"
    SERVER_PUBLIC_KEY = "keys\\public_server_key.txt"
    CERTIFIED_KEYS = "keys\\certified_keys.json"


class Messages:
    EXIT = "exit"
    NOT_CERTIFIED = "Ваш публичный ключ не сертифицирован"
    CERTIFIED = "Ваш публичный ключ сертифицирован"
    CHANGE_PORT = "Переключение на порт {}"
    REQUEST_LOGIN = "Введите логин:"
    REQUEST_PASSWORD = "Введите пароль:"
    REQUEST_NEW_PASSWORD = "Введите новый пароль:"
    INCORRECT_PASSWORD = "Неверный пароль"
    INCORRECT_PATH = "Такой путь не существует"
    CORRECT_PASSWORD = "Вход выполнен"
    LACK_OF_MEMORY = "Недостаточно места на диске"


class FileManagerSettings:
    import os
    SEP = os.sep
    WORKING_DIRECTORY = os.getcwd() + SEP + "file_manager"
    ADMIN = "admin"
    AUTH = WORKING_DIRECTORY + SEP + "auth.json"
    MAX_DIRECTORY_SIZE = 50
    LOG = WORKING_DIRECTORY + SEP + "log.txt"
