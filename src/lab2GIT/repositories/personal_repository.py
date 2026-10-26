import sqlite3
from Client import Client, Personal, Admin, Application


def get_connection():  # Получение конекшина к БД
    return sqlite3.connect('service1')


class PersonalRepository:
    def add(self, name, surname, patronymic, login, password):  # добавление сотрудника
        db = get_connection()
        cursor = db.cursor()
        cursor.execute('''INSERT INTO Personal (Name, Surname, Patronymic, Login, Password)
                          VALUES (?, ?, ?, ?, ?)''',
                       (name, surname, patronymic, login, password))
        db.commit()
        db.close()

    def get_by_id(self, kod_personal):  # поиск сотрудника по коду
        db = get_connection()
        cursor = db.cursor()
        cursor.execute('''SELECT * FROM Personal WHERE Kod_Personal = ?''', (kod_personal,))
        row = cursor.fetchone()
        db.close()
        if row is None:
            return None
        return Personal(*row)

    def get_all(self):  # все записи таблицы
        db = get_connection()
        cursor = db.cursor()
        cursor.execute('''SELECT * FROM Personal''')
        rows = cursor.fetchall()
        db.close()
        result = []
        for row in rows:
            result.append(Personal(*row))
        return result

    def update(self, kod_personal, name, surname, patronymic, login, password):  # изменение данных
        db = get_connection()
        cursor = db.cursor()
        cursor.execute('''UPDATE Personal
                          SET Name = ?, Surname = ?, Patronymic = ?, Login = ?, Password = ?
                          WHERE Kod_Personal = ?''',
                       (name, surname, patronymic, login, password, kod_personal))
        db.commit()
        db.close()

    def delete(self, kod_personal):  # удаление записи
        db = get_connection()
        cursor = db.cursor()
        cursor.execute('''DELETE FROM Personal WHERE Kod_Personal = ?''', (kod_personal,))
        db.commit()
        db.close()