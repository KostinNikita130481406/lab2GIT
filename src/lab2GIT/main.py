import sqlite3
from random import choice


def get_connection(): # Получение конекшина к БД
    return  sqlite3.connect('service')

def init_db():
    db = get_connection()
    cursor = db.cursor()
    # Таблица Клиентов
    cursor.execute('''CREATE TABLE IF NOT EXISTS Client (
                        Kod_client INTEGER PRIMARY KEY AUTOINCREMENT,
                        Full_Name STRING NOT NULL)''')
    #таблица сотрудников
    cursor.execute('''CREATE TABLE IF NOT EXISTS Personal (
                        Kod_Personal INTEGER PRIMARY KEY AUTOINCREMENT,
                        Full_Name TEXT NOT NULL)''')

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


def incert_client(FULL_NAME):
    db = get_connection()
    cursor = db.cursor()
    cursor.execute('''INSERT INTO Client (Full_Name)
                    VALUES (?) ''', (FULL_NAME,) )
    db.commit()
    db.close()

def Show_client():
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
                    VALUES (?) ''', (FULL_NAME,) )
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


def incert_application(Data_income,Type_electronics,Brand_name,Comment_problem,Kod_client):
    db = get_connection()
    cursor = db.cursor()
    cursor.execute('''INSERT INTO Application (Data_income,Type_electronics,Brand_name,Comment_problem,Kod_client)
                    VALUES (?,?,?,?,?)''', (Data_income,Type_electronics,Brand_name,Comment_problem,Kod_client))
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

# /////////////////////////////////////////////////////////////////////////////////////////////
print("Начало программы")
init_db()
while (True):
    print(" 1 - Завести клиента\n 2 - Завести сотрудника\n 3 - Завести заявку на ремонт\n 4 - Выйти из программы\n")
    choicee = int(input("Выберете вариант меню "))
    match choicee:
        case 1 :
            FULL_NAME = input("Введите ФИО клиента ")
            incert_client(FULL_NAME)
            Show_client()
        case 2:
            FULL_NAME = input("Введите ФИО сотрудника ")
            incert_personal(FULL_NAME)
            Show_personal()
        case 3:
            Data_income = input("Введите дату поступления заявки ")
            Type_electronics = input("Введите тип электротехники (Телефон, Телевизор, ПК и тд) ")
            Brand_name = input("Введите бренд техники (Bosh, LG, APPlE и тд ")
            Comment_problem = input("Введите описание проблемы с техникой ")
            print("Выберете клиента на которого будет назначена заявка ")
            Show_client()
            Kod_client = int(input())
            incert_application(Data_income,Type_electronics,Brand_name,Comment_problem,Kod_client)
            Show_application()
        case 4:
            print("Программа закрыта ")
            break
        case _:
            print("eerefe")



