import sqlite3
from models import Client, Personal, Admin, Application


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


class AdminRepository:
    def add(self, name, surname, patronymic, login, password):  # добавление администратора
        db = get_connection()
        cursor = db.cursor()
        cursor.execute('''INSERT INTO Admin (Name, Surname, Patronymic, Login, Password)
                          VALUES (?, ?, ?, ?, ?)''',
                       (name, surname, patronymic, login, password))
        db.commit()
        db.close()

    def get_by_id(self, kod_admin):  # поиск администратора по коду
        db = get_connection()
        cursor = db.cursor()
        cursor.execute('''SELECT * FROM Admin WHERE Kod_Admin = ?''', (kod_admin,))
        row = cursor.fetchone()
        db.close()
        if row is None:
            return None
        return Admin(*row)

    def get_all(self):  # все записи таблицы
        db = get_connection()
        cursor = db.cursor()
        cursor.execute('''SELECT * FROM Admin''')
        rows = cursor.fetchall()
        db.close()
        result = []
        for row in rows:
            result.append(Admin(*row))
        return result

    def update(self, kod_admin, name, surname, patronymic, login, password):  # изменение данных
        db = get_connection()
        cursor = db.cursor()
        cursor.execute('''UPDATE Admin
                          SET Name = ?, Surname = ?, Patronymic = ?, Login = ?, Password = ?
                          WHERE Kod_Admin = ?''',
                       (name, surname, patronymic, login, password, kod_admin))
        db.commit()
        db.close()

    def delete(self, kod_admin):  # удаление записи
        db = get_connection()
        cursor = db.cursor()
        cursor.execute('''DELETE FROM Admin WHERE Kod_Admin = ?''', (kod_admin,))
        db.commit()
        db.close()


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
        # В SQLite поиск не различает регистр только у латиницы, поэтому фильтруем в Python
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


if __name__ == "__main__":
    # Быстрая проверка: запустите этот файл, чтобы увидеть клиентов из базы
    print(ClientRepository().get_all())