import sqlite3
from Client import Client, Personal, Admin, Application


def get_connection():  # Получение конекшина к БД
    return sqlite3.connect('service1')
class ApplicationRepository:
    def add(self, Data_income, Type_electronics, Brand_name, Comment_problem, Kod_client, Kod_Personal=None):  # добавление заявки
        db = get_connection()
        cursor = db.cursor()
        cursor.execute('''INSERT INTO Application (Data_income, Type_electronics, Brand_name, Comment_problem, Kod_client, Kod_Personal)
                          VALUES (?, ?, ?, ?, ?, ?)''',
                       (Data_income, Type_electronics, Brand_name, Comment_problem, Kod_client, Kod_Personal))
        new_id = cursor.lastrowid  # номер только что созданной заявки
        db.commit()
        db.close()
        return new_id

    def get_by_id(self, ID_Application):  # поиск заявки по номеру
        db = get_connection()
        cursor = db.cursor()
        cursor.execute('''SELECT * FROM Application WHERE ID_Application = ?''', (ID_Application,))
        row = cursor.fetchone()
        db.close()
        if row is None:
            return None
        return Application(*row)

    def get_all(self):  # все заявки
        db = get_connection()
        cursor = db.cursor()
        cursor.execute('''SELECT * FROM Application ORDER BY Data_income ASC''')
        rows = cursor.fetchall()
        db.close()
        result = []
        for row in rows:
            result.append(Application(*row))
        return result

    def get_by_client(self, Kod_client):  # заявки одного клиента
        db = get_connection()
        cursor = db.cursor()
        cursor.execute('''SELECT * FROM Application
                          WHERE Kod_client = ?
                          ORDER BY Data_income ASC''', (Kod_client,))
        rows = cursor.fetchall()
        db.close()
        result = []
        for row in rows:
            result.append(Application(*row))
        return result

    def get_by_personal(self, Kod_Personal):  # заявки одного сотрудника
        db = get_connection()
        cursor = db.cursor()
        cursor.execute('''SELECT * FROM Application
                          WHERE Kod_Personal = ?
                          ORDER BY Data_income ASC''', (Kod_Personal,))
        rows = cursor.fetchall()
        db.close()
        result = []
        for row in rows:
            result.append(Application(*row))
        return result

    def count_open_by_personal(self, Kod_Personal):  # сколько у сотрудника незакрытых заявок
        db = get_connection()
        cursor = db.cursor()
        cursor.execute('''SELECT COUNT(*) FROM Application
                          WHERE Kod_Personal = ? AND Data_close IS NULL''', (Kod_Personal,))
        count = cursor.fetchone()[0]
        db.close()
        return count

    def update(self, ID_Application, Type_electronics, Brand_name, Comment_problem):  # изменение заявки
        db = get_connection()
        cursor = db.cursor()
        cursor.execute('''UPDATE Application
                          SET Type_electronics = ?, Brand_name = ?, Comment_problem = ?
                          WHERE ID_Application = ?''',
                       (Type_electronics, Brand_name, Comment_problem, ID_Application))
        db.commit()
        db.close()

    def assign(self, ID_Application, Kod_Personal):  # назначение сотрудника на заявку
        db = get_connection()
        cursor = db.cursor()
        cursor.execute('''UPDATE Application SET Kod_Personal = ?
                          WHERE ID_Application = ?''', (Kod_Personal, ID_Application))
        db.commit()
        db.close()

    def close(self, ID_Application, Data_close):  # закрытие заявки (дата закрытия)
        db = get_connection()
        cursor = db.cursor()
        cursor.execute('''UPDATE Application SET Data_close = ?
                          WHERE ID_Application = ?''', (Data_close, ID_Application))
        db.commit()
        db.close()

    def delete(self, ID_Application):  # удаление заявки
        db = get_connection()
        cursor = db.cursor()
        cursor.execute('''DELETE FROM Application WHERE ID_Application = ?''', (ID_Application,))
        db.commit()
        db.close()

    def search_by_type(self, text):  # поиск по виду техники
        result = []
        for application in self.get_all():
            if text.lower() in application.Type_electronics.lower():
                result.append(application)
        return result

    def search_by_client_name(self, text):  # поиск по ФИО клиента
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
