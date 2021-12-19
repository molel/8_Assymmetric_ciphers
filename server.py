import json
from socket import socket

from сipher import *
from filemanager import *


class Server:
    def __init__(self, sock, privateKey, publicKey, clientPublicKey):
        os.chdir(FileManagerSettings.WORKING_DIRECTORY)
        self.sock = sock
        self.sock.listen(1)
        self.privateKey = privateKey
        self.publicKey = publicKey
        self.clientPublicKey = clientPublicKey
        self.conn = None
        self.fileManager = None
        self.accept()

    def handle(self, login):
        self.checkDirectory(login)
        file_manager = FileManager(self.sock, self.conn, login)
        self.send(
            Messages.CORRECT_PASSWORD + "\n" + file_manager.login + "$" + file_manager.pwd()[:-1] + ">")
        self.writeLog(FileManagerSettings.LOG, f"Пользователь {file_manager.login} авторизовался")
        while True:
            try:
                request = self.recv()
                if request == "exit":
                    self.conn.close()
                response = file_manager.process(request)
                self.send(response)
                self.send(file_manager.login + "$" + file_manager.pwd()[:-1] + ">")
            except:
                break

        os.chdir(FileManagerSettings.WORKING_DIRECTORY)
        self.conn.close()

    @staticmethod
    def checkDirectory(login):
        login = FileManagerSettings.WORKING_DIRECTORY + FileManagerSettings.SEP + login
        if not os.path.exists(login) or not os.path.isdir(login):
            os.mkdir(login)
        os.chdir(login)

    @staticmethod
    def readAuth(fileName=FileManagerSettings.AUTH):
        with open(fileName, "r", encoding=GeneralSettings.ENCODING) as file:
            logins = json.load(file)
        return logins

    def writeAuth(self, fileName, data, currentPath=os.getcwd()):
        os.chdir(FileManagerSettings.WORKING_DIRECTORY)
        data.update(self.readAuth(fileName))
        json.dump(data, open(fileName, "w", encoding=GeneralSettings.ENCODING), sort_keys=True)
        os.chdir(currentPath)

    @staticmethod
    def writeLog(fileName, text):
        with open(fileName, "a", encoding=GeneralSettings.ENCODING) as logFile:
            logFile.write(f"{'-' * 25}\n{datetime.now()}: {text}\n")

    def requestPassword(self, correctPassword, login):
        password = self.makeRequest(Messages.REQUEST_PASSWORD)
        if password == correctPassword:
            self.handle(login)
        else:
            self.requestPassword(correctPassword, login)

    def requestNewPassword(self, login):
        newPassword = self.makeRequest(Messages.REQUEST_NEW_PASSWORD)
        self.writeAuth(FileManagerSettings.AUTH, {login: newPassword}, currentPath=os.getcwd())
        self.handle(login)

    def makeRequest(self, message):
        self.send(message)
        return self.recv()

    def send(self, message, encoding=GeneralSettings.ENCODING):
        self.conn.send(encrypt(encrypt(str(message), self.privateKey), self.publicKey).encode(encoding))

    def recv(self, bufSize=GeneralSettings.BUFFER_SIZE, encoding=GeneralSettings.ENCODING):
        return decrypt(decrypt(self.conn.recv(bufSize).decode(encoding), self.privateKey), self.clientPublicKey)

    def auth(self):
        logins = self.readAuth()
        login = self.makeRequest(Messages.REQUEST_LOGIN)
        if login in logins:
            self.requestPassword(logins[login], login)
        else:
            self.requestNewPassword(login)

    def accept(self):
        while True:
            try:
                self.conn = self.sock.accept()[0]
                self.auth()
            except Exception as e:
                print(str(e))
                continue


def main():
    sock = socket()
    sock.bind((GeneralSettings.HOST, GeneralSettings.ALTER_PORT))
    Server(sock, 0)


if __name__ == '__main__':
    main()
