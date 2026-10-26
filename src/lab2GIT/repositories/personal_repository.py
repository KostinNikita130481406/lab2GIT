from database.database import get_connection
from models.personal import Personal


def add(name, surname, patronymic, login, password):  # добавление сотрудника
    db = get_connection()
    cursor = db.cursor()
    cursor.execute('''INSERT INTO Personal (Name, Surname, Patronymic, Login, Password)
                      VALUES (?, ?, ?, ?, ?)''',
                   (name, surname, patronymic, login, password))
    db.commit()
    db.close()


def get_by_id(kod_personal):  # поиск сотрудника по коду
    db = get_connection()
    cursor = db.cursor()
    cursor.execute('''SELECT * FROM Personal WHERE Kod_Personal = ?''', (kod_personal,))
    row = cursor.fetchone()
    db.close()
    if row is None:
        return None
    return Personal(*row)


def get_all():  # все сотрудники
    db = get_connection()
    cursor = db.cursor()
    cursor.execute('''SELECT * FROM Personal''')
    rows = cursor.fetchall()
    db.close()
    result = []
    for row in rows:
        result.append(Personal(*row))
    return result


def update(kod_personal, name, surname, patronymic, login, password):  # изменение данных
    db = get_connection()
    cursor = db.cursor()
    cursor.execute('''UPDATE Personal
                      SET Name = ?, Surname = ?, Patronymic = ?, Login = ?, Password = ?
                      WHERE Kod_Personal = ?''',
                   (name, surname, patronymic, login, password, kod_personal))
    db.commit()
    db.close()


def delete(kod_personal):  # удаление сотрудника
    db = get_connection()
    cursor = db.cursor()
    cursor.execute('''DELETE FROM Personal WHERE Kod_Personal = ?''', (kod_personal,))
    db.commit()
    db.close()
