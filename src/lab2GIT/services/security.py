import hashlib


def hash_password(password):
    # пароль -> хеш (необратимая "мешанина" из 64 символов)
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def verify_password(password, password_hash):
    # хешируем то, что ввёл пользователь, и сравниваем с тем, что хранится
    return hash_password(password) == password_hash

