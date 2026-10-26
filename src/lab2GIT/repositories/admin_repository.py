from database.database import get_connection
from models.admin import Admin


def add(name, surname, patronymic, login, password):  # добавление администратора
    db = get_connection()
    cursor = db.cursor()
    cursor.execute('''INSERT INTO Admin (Name, Surname, Patronymic, Login, Password)
                      VALUES (?, ?, ?, ?, ?)''',
                   (name, surname, patronymic, login, password))
    db.commit()
    db.close()


def get_by_id(kod_admin):  # поиск администратора по коду
    db = get_connection()
    cursor = db.cursor()
    cursor.execute('''SELECT * FROM Admin WHERE Kod_Admin = ?''', (kod_admin,))
    row = cursor.fetchone()
    db.close()
    if row is None:
        return None
    return Admin(*row)


def get_all():  # все администраторы
    db = get_connection()
    cursor = db.cursor()
    cursor.execute('''SELECT * FROM Admin''')
    rows = cursor.fetchall()
    db.close()
    result = []
    for row in rows:
        result.append(Admin(*row))
    return result


def update(kod_admin, name, surname, patronymic, login, password):  # изменение данных
    db = get_connection()
    cursor = db.cursor()
    cursor.execute('''UPDATE Admin
                      SET Name = ?, Surname = ?, Patronymic = ?, Login = ?, Password = ?
                      WHERE Kod_Admin = ?''',
                   (name, surname, patronymic, login, password, kod_admin))
    db.commit()
    db.close()


def delete(kod_admin):  # удаление администратора
    db = get_connection()
    cursor = db.cursor()
    cursor.execute('''DELETE FROM Admin WHERE Kod_Admin = ?''', (kod_admin,))
    db.commit()
    db.close()
