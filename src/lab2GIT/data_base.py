import sqlite3
from dataclasses import dataclass

@dataclass
class User:
    User_id: int
    loginn: str
    password: str
    Type_User: int
    name: str
    surname: str
    patronymic: str

def get_connection():  # Получение конекшина к БД
    return sqlite3.connect('service1')


def init_db():
    db = get_connection()
    cursor = db.cursor()
    # Таблица Клиентов
    cursor.execute('''CREATE TABLE IF NOT EXISTS Client (
                        Kod_client INTEGER PRIMARY KEY AUTOINCREMENT,
                        Name STRING NOT NULL,
                        Surname STRING NOT NULL,
                        Patronymic STRING,
                        Login STRING NOT NULL,
                        Password STRING NOT NULL)''')
    # таблица сотрудников
    cursor.execute('''CREATE TABLE IF NOT EXISTS Personal (
                        Kod_Personal INTEGER PRIMARY KEY AUTOINCREMENT,
                        Name STRING NOT NULL,
                        Surname STRING NOT NULL,
                        Patronymic STRING,
                        Login STRING NOT NULL,
                        Password STRING NOT NULL)''')

    #Таблица администратора
    cursor.execute('''CREATE TABLE IF NOT EXISTS Admin (
                        Kod_Admin INTEGER PRIMARY KEY AUTOINCREMENT,
                        Name STRING NOT NULL,
                        Surname STRING NOT NULL,
                        Patronymic STRING,
                        Login STRING NOT NULL,
                        Password STRING NOT NULL)''')

    #Таблица заявок
    cursor.execute('''CREATE TABLE IF NOT EXISTS Application (
                        ID_Application INTEGER PRIMARY KEY AUTOINCREMENT,
                        Data_income TEXT NOT NULL,
                        Type_electronics TEXT NOT NULL,
                        Brand_name TEXT NOT NULL,
                        Comment_problem TEXT NOT NULL,
                        Data_close TEXT,
                        Kod_client INTEGER NOT NULL,
                        Kod_Personal INTEGER,

                        FOREIGN KEY (Kod_Personal)
                            REFERENCES Personal (Kod_Personal), 

                        FOREIGN KEY (Kod_client)
                            REFERENCES Client (Kod_client))''')
    db.commit()
    db.close()


def incert_client(name, surname, patronymic, login, password):  # функция добавления клиента
    db = get_connection()
    cursor = db.cursor()
    cursor.execute('''INSERT INTO Client (Name, Surname, Patronymic, Login, Password)
                          VALUES (?, ?, ?, ?, ?)''',
                   (name, surname, patronymic, login, password))
    db.commit()
    db.close()


def Show_client():  # вывод всех клиентов
    db = get_connection()
    cursor = db.cursor()
    cursor.execute('''SELECT * FROM Client''')
    rows = cursor.fetchall()
    for row in rows:
        print(*row)
    print("")
    db.close()


def incert_personal(name, surname, patronymic, login, password):
    db = get_connection()
    cursor = db.cursor()
    cursor.execute('''INSERT INTO Personal (Name, Surname, Patronymic, Login, Password)
                      VALUES (?, ?, ?, ?, ?)''',
                   (name, surname, patronymic, login, password))
    db.commit()
    db.close()


def Show_personal():
    db = get_connection()
    cursor = db.cursor()
    cursor.execute('''SELECT * FROM Personal''')
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    db.close()



def incert_Admin(name, surname, patronymic, login, password):
    db = get_connection()
    cursor = db.cursor()
    cursor.execute('''INSERT INTO Admin (Name, Surname, Patronymic, Login, Password)
                      VALUES (?, ?, ?, ?, ?)''',
                   (name, surname, patronymic, login, password))
    db.commit()
    db.close()


def Show_Admin():
    db = get_connection()
    cursor = db.cursor()
    cursor.execute('''SELECT * FROM Admin''')
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    db.close()

def incert_application(Data_income, Type_electronics, Brand_name, Comment_problem, Kod_client):
    db = get_connection()
    cursor = db.cursor()
    cursor.execute('''INSERT INTO Application (Data_income,Type_electronics,Brand_name,Comment_problem,Kod_client)
                    VALUES (?,?,?,?,?)''', (Data_income, Type_electronics, Brand_name, Comment_problem, Kod_client))
    db.commit()
    db.close()


def Show_application():
    db = get_connection()
    cursor = db.cursor()
    cursor.execute('''SELECT ID_Application, Data_income,Type_electronics,Brand_name,Comment_problem,Kod_client 
                    FROM Application 
                    ORDER BY Data_income ASC''')

    rows = cursor.fetchall()
    for row in rows:
        print(row)
    db.close()

#############################################
def Redistration_User(user):
    Login = user.loginn

    while(True):
        rezult = Find_login_Password(Login)
        if rezult == None:
            #incert_client(user.name, user.surname, user.patronymic, Login, user.password)
            incert_personal(user.name, user.surname, user.name, Login, user.password)
            #incert_Admin(user.name, user.surname, user.name, Login, user.password)
            break
        else:
            print("Такой логин уже существует. Придумайте новый логин ")
            Login = input()





#############################################
def Find_login_Password(login, password = None):
    user_Client = Find_Client(login, password = None)
    user_Personal = Find_Personal(login, password = None)
    user_admin = Find_Admin(login, password = None)

    if user_Client is None and user_Personal is None and user_admin is None:
        return None
    Role = []
    Role.append(user_Client)
    Role.append(user_Personal)
    Role.append(user_admin)
    return Role

# Поиск логина по таблицам данных
def Find_Client(login,password = None):
    db = get_connection()
    cursor = db.cursor()
    if password != None:
        cursor.execute('''SELECT * FROM Client 
            WHERE Login = ? 
            AND Password = ?''', (login, password))
    else :
        cursor.execute('''SELECT * FROM Client 
        WHERE Login = ? ''', (login,))

    User = cursor.fetchone()
    if User:
        user = User[0]
        return user
    else:
        return None

def Find_Personal(login,password = None):
    db = get_connection()
    cursor = db.cursor()
    if password != None:
        cursor.execute('''SELECT * FROM Personal 
             WHERE Login = ? 
             AND Password = ?''', (login, password))
    else:
        cursor.execute('''SELECT * FROM Personal 
                     WHERE Login = ? ''', (login,))
    User = cursor.fetchone()
    if User:
        user = User[0]
        return user
    else:
        return None

def Find_Admin(login,password = None):
    db = get_connection()
    cursor = db.cursor()
    if password != None:
        cursor.execute('''SELECT * FROM Admin 
             WHERE Login = ? 
             AND Password = ?''', (login, password))
    else:
        cursor.execute('''SELECT * FROM Client 
         WHERE Login = ? ''', (login,))
    User = cursor.fetchone()
    if User:
        user = User[0]
        return user
    else:
        return None

