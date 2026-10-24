import sqlite3
from models import Client, Personal, Admin, Application


def get_connection():
    return sqlite3.connect('service1')


class ClientRepository:
    def add(self, name, surname, patronymic, login, password):
        db = get_connection()
        cursor = db.cursor()
        cursor.execute('''INSERT INTO Client (Name, Surname, Patronymic, Login, Password)
                          VALUES (?, ?, ?, ?, ?)''',
                       (name, surname, patronymic, login, password))
        db.commit()
        db.close()

    def get_by_id(self, kod_client):
        db = get_connection()
        cursor = db.cursor()
        cursor.execute('''SELECT * FROM Client WHERE Kod_client = ?''', (kod_client,))
        row = cursor.fetchone()
        db.close()
        return Client(*row) if row else None

    def get_all(self):
        db = get_connection()
        cursor = db.cursor()
        cursor.execute('''SELECT * FROM Client''')
        rows = cursor.fetchall()
        db.close()
        return [Client(*row) for row in rows]

    def update(self, kod_client, name, surname, patronymic, login, password):
        db = get_connection()
        cursor = db.cursor()
        cursor.execute('''UPDATE Client
                          SET Name = ?, Surname = ?, Patronymic = ?, Login = ?, Password = ?
                          WHERE Kod_client = ?''',
                       (name, surname, patronymic, login, password, kod_client))
        db.commit()
        db.close()

    def delete(self, kod_client):
        db = get_connection()
        cursor = db.cursor()
        cursor.execute('''DELETE FROM Client WHERE Kod_client = ?''', (kod_client,))
        db.commit()
        db.close()


class PersonalRepository:
    def add(self, name, surname, patronymic, login, password):
        db = get_connection()
        cursor = db.cursor()
        cursor.execute('''INSERT INTO Personal (Name, Surname, Patronymic, Login, Password)
                          VALUES (?, ?, ?, ?, ?)''',
                       (name, surname, patronymic, login, password))
        db.commit()
        db.close()

    def get_by_id(self, kod_personal):
        db = get_connection()
        cursor = db.cursor()
        cursor.execute('''SELECT * FROM Personal WHERE Kod_Personal = ?''', (kod_personal,))
        row = cursor.fetchone()
        db.close()
        return Personal(*row) if row else None

    def get_all(self):
        db = get_connection()
        cursor = db.cursor()
        cursor.execute('''SELECT * FROM Personal''')
        rows = cursor.fetchall()
        db.close()
        return [Personal(*row) for row in rows]

    def update(self, kod_personal, name, surname, patronymic, login, password):
        db = get_connection()
        cursor = db.cursor()
        cursor.execute('''UPDATE Personal
                          SET Name = ?, Surname = ?, Patronymic = ?, Login = ?, Password = ?
                          WHERE Kod_Personal = ?''',
                       (name, surname, patronymic, login, password, kod_personal))
        db.commit()
        db.close()

    def delete(self, kod_personal):
        db = get_connection()
        cursor = db.cursor()
        cursor.execute('''DELETE FROM Personal WHERE Kod_Personal = ?''', (kod_personal,))
        db.commit()
        db.close()


class AdminRepository:
    def add(self, name, surname, patronymic, login, password):
        db = get_connection()
        cursor = db.cursor()
        cursor.execute('''INSERT INTO Admin (Name, Surname, Patronymic, Login, Password)
                          VALUES (?, ?, ?, ?, ?)''',
                       (name, surname, patronymic, login, password))
        db.commit()
        db.close()

    def get_by_id(self, kod_admin):
        db = get_connection()
        cursor = db.cursor()
        cursor.execute('''SELECT * FROM Admin WHERE Kod_Admin = ?''', (kod_admin,))
        row = cursor.fetchone()
        db.close()
        return Admin(*row) if row else None

    def get_all(self):
        db = get_connection()
        cursor = db.cursor()
        cursor.execute('''SELECT * FROM Admin''')
        rows = cursor.fetchall()
        db.close()
        return [Admin(*row) for row in rows]

    def update(self, kod_admin, name, surname, patronymic, login, password):
        db = get_connection()
        cursor = db.cursor()
        cursor.execute('''UPDATE Admin
                          SET Name = ?, Surname = ?, Patronymic = ?, Login = ?, Password = ?
                          WHERE Kod_Admin = ?''',
                       (name, surname, patronymic, login, password, kod_admin))
        db.commit()
        db.close()

    def delete(self, kod_admin):
        db = get_connection()
        cursor = db.cursor()
        cursor.execute('''DELETE FROM Admin WHERE Kod_Admin = ?''', (kod_admin,))
        db.commit()
        db.close()


class ApplicationRepository:
    def add(self, data_income, type_electronics, brand_name, comment_problem, kod_client, kod_personal=None):
        db = get_connection()
        cursor = db.cursor()
        cursor.execute('''INSERT INTO Application
                          (Data_income, Type_electronics, Brand_name, Comment_problem, Kod_client, Kod_Personal)
                          VALUES (?, ?, ?, ?, ?, ?)''',
                       (data_income, type_electronics, brand_name, comment_problem, kod_client, kod_personal))
        new_id = cursor.lastrowid
        db.commit()
        db.close()
        return new_id

    def get_by_id(self, id_application):
        db = get_connection()
        cursor = db.cursor()
        cursor.execute('''SELECT * FROM Application WHERE ID_Application = ?''', (id_application,))
        row = cursor.fetchone()
        db.close()
        return Application(*row) if row else None

    def get_all(self):
        db = get_connection()
        cursor = db.cursor()
        cursor.execute('''SELECT * FROM Application ORDER BY Data_income ASC''')
        rows = cursor.fetchall()
        db.close()
        return [Application(*row) for row in rows]

    def get_by_client(self, kod_client):
        db = get_connection()
        cursor = db.cursor()
        cursor.execute('''SELECT * FROM Application WHERE Kod_client = ?
                          ORDER BY Data_income ASC''', (kod_client,))
        rows = cursor.fetchall()
        db.close()
        return [Application(*row) for row in rows]

    def get_by_personal(self, kod_personal):
        db = get_connection()
        cursor = db.cursor()
        cursor.execute('''SELECT * FROM Application WHERE Kod_Personal = ?
                          ORDER BY Data_income ASC''', (kod_personal,))
        rows = cursor.fetchall()
        db.close()
        return [Application(*row) for row in rows]

    def count_open_by_personal(self, kod_personal):
        db = get_connection()
        cursor = db.cursor()
        cursor.execute('''SELECT COUNT(*) FROM Application
                          WHERE Kod_Personal = ? AND Data_close IS NULL''', (kod_personal,))
        count = cursor.fetchone()[0]
        db.close()
        return count

    def update(self, id_application, type_electronics, brand_name, comment_problem):
        db = get_connection()
        cursor = db.cursor()
        cursor.execute('''UPDATE Application
                          SET Type_electronics = ?, Brand_name = ?, Comment_problem = ?
                          WHERE ID_Application = ?''',
                       (type_electronics, brand_name, comment_problem, id_application))
        db.commit()
        db.close()

    def assign(self, id_application, kod_personal):
        db = get_connection()
        cursor = db.cursor()
        cursor.execute('''UPDATE Application SET Kod_Personal = ?
                          WHERE ID_Application = ?''', (kod_personal, id_application))
        db.commit()
        db.close()

    def close(self, id_application, data_close):
        db = get_connection()
        cursor = db.cursor()
        cursor.execute('''UPDATE Application SET Data_close = ?
                          WHERE ID_Application = ?''', (data_close, id_application))
        db.commit()
        db.close()

    def delete(self, id_application):
        db = get_connection()
        cursor = db.cursor()
        cursor.execute('''DELETE FROM Application WHERE ID_Application = ?''', (id_application,))
        db.commit()
        db.close()

    def search_by_type(self, text):
        db = get_connection()
        db.create_function("py_lower", 1, lambda s: s.lower() if s else "")
        cursor = db.cursor()
        cursor.execute('''SELECT * FROM Application WHERE py_lower(Type_electronics) LIKE ?
                          ORDER BY Data_income ASC''', (f"%{text.lower()}%",))
        rows = cursor.fetchall()
        db.close()
        return [Application(*row) for row in rows]

    def search_by_client_name(self, text):
        db = get_connection()
        db.create_function("py_lower", 1, lambda s: s.lower() if s else "")
        cursor = db.cursor()
        cursor.execute('''SELECT Application.* FROM Application
                          JOIN Client ON Client.Kod_client = Application.Kod_client
                          WHERE py_lower(Client.Surname || ' ' || Client.Name || ' ' ||
                                         COALESCE(Client.Patronymic, '')) LIKE ?
                          ORDER BY Application.Data_income ASC''', (f"%{text.lower()}%",))
        rows = cursor.fetchall()
        db.close()
        return [Application(*row) for row in rows]


if __name__ == "__main__":
    # Быстрая проверка: запустите этот файл, чтобы увидеть клиентов из базы
    print(ClientRepository().get_all())