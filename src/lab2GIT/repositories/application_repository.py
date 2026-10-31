from database.database import get_connection
from models.application import Application


def add(data_income, type_electronics, brand_name, comment_problem, kod_client, kod_personal=None):  # добавление заявки
    db = get_connection()
    cursor = db.cursor()
    cursor.execute('''INSERT INTO Application (Data_income, Type_electronics, Brand_name, Comment_problem, Kod_client, Kod_Personal)
                      VALUES (?, ?, ?, ?, ?, ?)''',
                   (data_income, type_electronics, brand_name, comment_problem, kod_client, kod_personal))
    new_id = cursor.lastrowid  # номер только что созданной заявки
    db.commit()
    db.close()
    return new_id


def get_by_id(id_application):  # поиск заявки по номеру
    db = get_connection()
    cursor = db.cursor()
    cursor.execute('''SELECT * FROM Application WHERE ID_Application = ?''', (id_application,))
    row = cursor.fetchone()
    db.close()
    if row is None:
        return None
    return Application(*row)

def get_ALL_by_unload():
    pass

def get_all():  # все заявки
    db = get_connection()
    cursor = db.cursor()
    cursor.execute('''SELECT * FROM Application ORDER BY Data_income ASC''')
    rows = cursor.fetchall()
    db.close()
    result = []
    for row in rows:
        result.append(Application(*row))
    return result


def get_by_client(kod_client):  # заявки одного клиента
    db = get_connection()
    cursor = db.cursor()
    cursor.execute('''SELECT * FROM Application
                      WHERE Kod_client = ?
                      ORDER BY Data_income ASC''', (kod_client,))
    rows = cursor.fetchall()
    db.close()
    result = []
    for row in rows:
        result.append(Application(*row))
    return result


def get_by_personal(kod_personal):  # заявки одного сотрудника
    db = get_connection()
    cursor = db.cursor()
    cursor.execute('''SELECT * FROM Application
                      WHERE Kod_Personal = ?
                      ORDER BY Data_income ASC''', (kod_personal,))
    rows = cursor.fetchall()
    db.close()
    result = []
    for row in rows:
        result.append(Application(*row))
    return result


def count_open_by_personal(kod_personal):  # сколько у сотрудника незакрытых заявок
    db = get_connection()
    cursor = db.cursor()
    cursor.execute('''SELECT COUNT(*) FROM Application
                      WHERE Kod_Personal = ? AND Data_close IS NULL''', (kod_personal,))
    count = cursor.fetchone()[0]
    db.close()
    return count


def update(id_application, type_electronics, brand_name, comment_problem):  # изменение заявки
    db = get_connection()
    cursor = db.cursor()
    cursor.execute('''UPDATE Application
                      SET Type_electronics = ?, Brand_name = ?, Comment_problem = ?
                      WHERE ID_Application = ?''',
                   (type_electronics, brand_name, comment_problem, id_application))
    db.commit()
    db.close()


def assign(id_application, kod_personal):  # назначение сотрудника на заявку
    db = get_connection()
    cursor = db.cursor()
    cursor.execute('''UPDATE Application SET Kod_Personal = ?
                      WHERE ID_Application = ?''', (kod_personal, id_application))
    db.commit()
    db.close()


def close(id_application, data_close):  # закрытие заявки (дата закрытия)
    db = get_connection()
    cursor = db.cursor()
    cursor.execute('''UPDATE Application SET Data_close = ?
                      WHERE ID_Application = ?''', (data_close, id_application))
    db.commit()
    db.close()


def delete(id_application):  # удаление заявки
    db = get_connection()
    cursor = db.cursor()
    cursor.execute('''DELETE FROM Application WHERE ID_Application = ?''', (id_application,))
    db.commit()
    db.close()


def search_by_type(text):  # поиск по виду техники
    result = []
    for application in get_all():
        if text.lower() in application.Type_electronics.lower():
            result.append(application)
    return result


def search_by_client_name(text):  # поиск по ФИО клиента
    db = get_connection()
    cursor = db.cursor()
    cursor.execute('''SELECT Application.*, Client.Surname, Client.Name, Client.Patronymic
                      FROM Application
                      JOIN Client ON Client.Kod_client = Application.Kod_client
                      ORDER BY Application.Data_income ASC''')
    rows = cursor.fetchall()
    db.close()
    result = []
    for row in rows:
        full_name = f"{row[8]} {row[9]} {row[10] or ''}"  # Фамилия Имя Отчество
        if text.lower() in full_name.lower():
            result.append(Application(*row[:8]))  # первые 8 значений это сама заявка
    return result
