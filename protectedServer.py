from json import load
from socket import socket

from server import Server
from settings import GeneralSettings, PathsStorage, Messages


def getKey(path):
    with open(path, "r", encoding=GeneralSettings.ENCODING) as file:
        return int(file.read())


def getCertifiedKeys():
    with open(PathsStorage.CERTIFIED_KEYS, "r", encoding=GeneralSettings.ENCODING) as file:
        return load(file)


class ProtectedServer:
    def __init__(self):
        self.publicKey = getKey(PathsStorage.SERVER_PUBLIC_KEY)
        self.certifiedKeys = getCertifiedKeys()

        self.sock = socket()
        self.sock.bind((GeneralSettings.HOST, GeneralSettings.PORT))
        self.sock.listen(1)
        self.conn = None
        self.accept()

    def recv(self):
        return self.conn.recv(GeneralSettings.BUFFER_SIZE).decode(GeneralSettings.ENCODING)

    def send(self, text):
        self.conn.send(text.encode(GeneralSettings.ENCODING))

    def accept(self):
        while True:
            self.conn = self.sock.accept()[0]
            self.checkKey()

    def checkKey(self):
        clientPublicKey = self.recv()
        if clientPublicKey in self.certifiedKeys.keys():
            privateKey = int(self.certifiedKeys[clientPublicKey])
            publicKey = getKey(PathsStorage.SERVER_PUBLIC_KEY)
            clientPublicKey = int(clientPublicKey)
            sock, port = self.getPort()
            self.send(str(port))
            Server(sock, privateKey, publicKey, clientPublicKey)
        else:
            self.send(Messages.NOT_CERTIFIED)

    @staticmethod
    def getPort():
        sock = socket()
        for port in range(GeneralSettings.MIN_PORT, GeneralSettings.MAX_PORT):
            try:
                sock.bind((GeneralSettings.HOST, port))
            except:
                continue
            finally:
                return sock, port


def main():
    ProtectedServer()


if __name__ == '__main__':
    main()
