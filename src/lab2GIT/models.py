from dataclasses import dataclass


@dataclass
class Client:
    Kod_client: int
    Name: str
    Surname: str
    Patronymic: str|None
    Login: str
    Password: str

@dataclass
class Personal:
    Kod_Personal:int
    Name:str
    Surname:str
    Patronymic:str|None
    Login:str
    Password:str


@dataclass
class Admin:
    Kod_Admin:int
    Name:str
    Surname:str
    Patronymic:str|None
    Login:str
    Password:str

@dataclass
class Application:
    ID_Application:int
    Data_income: str
    Type_electronics:str
    Brand_name:str
    Comment_problem:str
    Data_close:str|None
    Kod_client:int
    Kod_Personal:int|None
