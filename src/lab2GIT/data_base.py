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
    return sqlite3.connect('service')


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
                        ID_Application INTEGER PRIMARY KEY AUTOINCREMENT,у
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


def incert_client(FULL_NAME):  # функция добавления клиента
    db = get_connection()
    cursor = db.cursor()
    cursor.execute('''INSERT INTO Client (Full_Name)
                    VALUES (?) ''', (FULL_NAME,))
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


def incert_personal(FULL_NAME):
    db = get_connection()
    cursor = db.cursor()
    cursor.execute('''INSERT INTO Personal (Full_Name)
                    VALUES (?) ''', (FULL_NAME,))
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
def Redistration_User():





#############################################
def Find_login_Password(login,password):
    User = Find_Client(login,password)
    if User == None:
        User = Find_Personal(login,password)
    else:
        return User


        #if User == None:
         #   User = Find_Admin(login,password)
         #   if User == None:
        #        return False

def Find_Client(login,password):
    db = get_connection()
    cursor = db.cursor()
    cursor.execute('''SELECT * FROM Client 
                    WHERE Login = ? 
                    AND Password = ?''', (login, password))

    User = cursor.fetchone()
    if User:
        user = User[0]
        return user
    else:
        return None

def Find_Personal(login,password):
    db = get_connection()
    cursor = db.cursor()
    cursor.execute('''SELECT * FROM Personal 
                    WHERE Login = ? 
                    AND Password = ?''', (login, password))

def Find_Admin(login,password):
    db = get_connection()
    cursor = db.cursor()
    cursor.execute('''SELECT * FROM Admin 
                    WHERE Login = ? 
                    AND Password = ?''', (login, password))

