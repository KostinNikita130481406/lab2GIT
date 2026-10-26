CREATE TABLE IF NOT EXISTS Client (
    Kod_client INTEGER PRIMARY KEY AUTOINCREMENT,
    Name STRING NOT NULL,
    Surname STRING NOT NULL,
    Patronymic STRING,
    Login STRING NOT NULL,
    Password STRING NOT NULL
);

CREATE TABLE IF NOT EXISTS Personal (
    Kod_Personal INTEGER PRIMARY KEY AUTOINCREMENT,
    Name STRING NOT NULL,
    Surname STRING NOT NULL,
    Patronymic STRING,
    Login STRING NOT NULL,
    Password STRING NOT NULL
);

CREATE TABLE IF NOT EXISTS Admin (
    Kod_Admin INTEGER PRIMARY KEY AUTOINCREMENT,
    Name STRING NOT NULL,
    Surname STRING NOT NULL,
    Patronymic STRING,
    Login STRING NOT NULL,
    Password STRING NOT NULL
);

CREATE TABLE IF NOT EXISTS Application (
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
        REFERENCES Client (Kod_client)
);
