from database.database import get_connection
from models.client import Client


def add(name, surname, patronymic, login, password):  # добавление клиента
    db = get_connection()
    cursor = db.cursor()
    cursor.execute('''INSERT INTO Client (Name, Surname, Patronymic, Login, Password)
                      VALUES (?, ?, ?, ?, ?)''',
                   (name, surname, patronymic, login, password))
    db.commit()
    db.close()


def get_by_id(kod_client):  # поиск клиента по коду
    db = get_connection()
    cursor = db.cursor()
    cursor.execute('''SELECT * FROM Client WHERE Kod_client = ?''', (kod_client,))
    row = cursor.fetchone()
    db.close()
    if row is None:
        return None
    return Client(*row)


def get_all():  # все клиенты
    db = get_connection()
    cursor = db.cursor()
    cursor.execute('''SELECT * FROM Client''')
    rows = cursor.fetchall()
    db.close()
    result = []
    for row in rows:
        result.append(Client(*row))
    return result


def update(kod_client, name, surname, patronymic, login, password):  # изменение данных
    db = get_connection()
    cursor = db.cursor()
    cursor.execute('''UPDATE Client
                      SET Name = ?, Surname = ?, Patronymic = ?, Login = ?, Password = ?
                      WHERE Kod_client = ?''',
                   (name, surname, patronymic, login, password, kod_client))
    db.commit()
    db.close()


def delete(kod_client):  # удаление клиента
    db = get_connection()
    cursor = db.cursor()
    cursor.execute('''DELETE FROM Client WHERE Kod_client = ?''', (kod_client,))
    db.commit()
    db.close()
