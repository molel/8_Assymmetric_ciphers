from json import dump, load
from random import randint as rand

from settings import PathsStorage, GeneralSettings


def generateKey(power, base, remainder):
    return base ** power % remainder


def saveKey(path, key):
    with open(path, 'w', encoding=GeneralSettings.ENCODING) as file:
        file.write(str(key))


def saveCertifiedKey(clientPublicKey, serverPrivateKey):
    with open(PathsStorage.CERTIFIED_KEYS, "r", encoding=GeneralSettings.ENCODING) as file:
        keys = load(file)

    keys[clientPublicKey] = str(serverPrivateKey)

    with open(PathsStorage.CERTIFIED_KEYS, "w", encoding=GeneralSettings.ENCODING) as file:
        dump(keys, file)


def main():
    p = 123456
    g = 5
    a = rand(2, p - 1)
    b = rand(2, p - 1)

    clientPublicKey = generateKey(a, g, p)
    serverPublicKey = generateKey(b, g, p)

    clientPrivateKey = generateKey(a, serverPublicKey, p)
    serverPrivateKey = generateKey(a, serverPublicKey, p)

    saveCertifiedKey(clientPublicKey, serverPrivateKey)
    saveKey(PathsStorage.CLIENT_PUBLIC_KEY, clientPublicKey)
    saveKey(PathsStorage.CLIENT_PRIVATE_KEY, clientPrivateKey)
    saveKey(PathsStorage.SERVER_PUBLIC_KEY, serverPublicKey)


if __name__ == '__main__':
    main()
