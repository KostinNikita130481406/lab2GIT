import sqlite3
from pathlib import Path

DB_NAME = "service1"


def get_connection():  # Получение конекшина к БД
    return sqlite3.connect(DB_NAME)


def init_db():
    # Сам SQL лежит в schema.sql, здесь только его загрузка и выполнение
    db = get_connection()

    sql_path = Path(__file__).parent / "schema.sql"
    with open(sql_path, "r", encoding="utf-8") as file:
        sql_script = file.read()

    db.executescript(sql_script)
    db.commit()
    db.close()
