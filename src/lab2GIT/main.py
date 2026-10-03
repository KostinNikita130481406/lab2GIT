import sqlite3

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
