from socket import socket

from Cipher import *
from protectedServer import getKey
from settings import PathsStorage, GeneralSettings, Messages


def recv(sock, privateKey, publicServerKey, encoding=GeneralSettings.ENCODING):
    print("-" * 50)
    message = sock.recv(GeneralSettings.BUFFER_SIZE).decode(encoding)
    print(f"Пришло:\n{message}")
    message = decrypt(decrypt(message, privateKey), publicServerKey)
    print(f"После расшифровки:\n{message}")
    print("-" * 50)
    return message


def send(sock, text, privateKey, publicKey, encoding=GeneralSettings.ENCODING):
    sock.send(encrypt(encrypt(text, privateKey), publicKey).encode(encoding))


def auth(sock, privateKey, publicKey, publicServerKey):
    while True:
        response = recv(sock, privateKey, publicServerKey)
        print(response, end="")
        if Messages.CORRECT_PASSWORD in response:
            break
        print()
        request = input('>')
        send(sock, request, privateKey, publicKey)


def process(sock):
    privateKey = getKey(PathsStorage.CLIENT_PRIVATE_KEY)
    publicKey = getKey(PathsStorage.CLIENT_PUBLIC_KEY)
    publicServerKey = getKey(PathsStorage.SERVER_PUBLIC_KEY)
    auth(sock, privateKey, publicKey, publicServerKey)
    with sock:
        while True:
            request = input()
            send(sock, request, privateKey, publicKey)
            if request == Messages.EXIT:
                break
            response = recv(sock, privateKey, publicServerKey)
            print(response, end="")
            response = recv(sock, privateKey, publicServerKey)
            print(response, end="")


def main():
    publicKey = getKey(PathsStorage.CLIENT_PUBLIC_KEY)
    sock = socket()
    sock.connect((GeneralSettings.HOST, GeneralSettings.PORT))
    sock.send(str(publicKey).encode(GeneralSettings.ENCODING))
    response = sock.recv(GeneralSettings.BUFFER_SIZE).decode(GeneralSettings.ENCODING)
    sock.close()
    if response.isnumeric():
        sock = socket()
        sock.connect((GeneralSettings.HOST, int(response)))
        process(sock)


if __name__ == '__main__':
    main()
