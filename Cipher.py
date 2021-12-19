from settings import CipherSettings


def get_chars(ords):
    return list(map(chr, ords))


def get_ords(chars):
    return list(map(ord, chars))


def encrypt(text, key=CipherSettings.MAX_ORD):
    return "".join(get_chars([char ^ key for char in get_ords(text)]))


def decrypt(text, key=CipherSettings.MAX_ORD):
    return encrypt(text, key)
