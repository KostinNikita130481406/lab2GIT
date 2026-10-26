import sqlite3
from Client import Client, Personal, Admin, Application


def get_connection():  # Получение конекшина к БД
    return sqlite3.connect('service1')
class ClientRepository:
    def add(self, name, surname, patronymic, login, password):  # добавление клиента
        db = get_connection()
        cursor = db.cursor()
        cursor.execute('''INSERT INTO Client (Name, Surname, Patronymic, Login, Password)
                          VALUES (?, ?, ?, ?, ?)''',
                       (name, surname, patronymic, login, password))
        db.commit()
        db.close()

    def get_by_id(self, kod_client):  # поиск клиента по коду
        db = get_connection()
        cursor = db.cursor()
        cursor.execute('''SELECT * FROM Client WHERE Kod_client = ?''', (kod_client,))
        row = cursor.fetchone()
        db.close()
        if row is None:
            return None
        return Client(*row)

    def get_all(self):  # все записи таблицы
        db = get_connection()
        cursor = db.cursor()
        cursor.execute('''SELECT * FROM Client''')
        rows = cursor.fetchall()
        db.close()
        result = []
        for row in rows:
            result.append(Client(*row))
        return result

    def update(self, kod_client, name, surname, patronymic, login, password):  # изменение данных
        db = get_connection()
        cursor = db.cursor()
        cursor.execute('''UPDATE Client
                          SET Name = ?, Surname = ?, Patronymic = ?, Login = ?, Password = ?
                          WHERE Kod_client = ?''',
                       (name, surname, patronymic, login, password, kod_client))
        db.commit()
        db.close()

    def delete(self, kod_client):  # удаление записи
        db = get_connection()
        cursor = db.cursor()
        cursor.execute('''DELETE FROM Client WHERE Kod_client = ?''', (kod_client,))
        db.commit()
        db.close()
