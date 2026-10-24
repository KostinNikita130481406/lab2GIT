import data_base
from dataclasses import dataclass

@dataclass
class User:
    User_id: int
    loginn: str
    password: str
    name: str
    surname: str
    patronymic: str

def registration_login():
    print("1 - Войти в систему\n 2 - Зарегистрироваться в системе\n ")
    chosee = int(input('Выберете пункт меню'))
    match chosee:
        case 1:
            login()
            print(Role)
            #функция вызова основного меню клиента
        case 2:
            Registration()




def login():
    global Role
    while True:
        Loginn = input("Введите логин: ")
        password = input("Введите пароль: ")
        clean_login = Loginn.strip()
        clean_password = password.strip()
        if clean_login and clean_password:
            users = data_base.Find_login_Password(clean_login, clean_password)
            if users != None:
                #Проверка роли пользователя
                print(users)
                if users[0] != None:
                    Role = "Клиент"
                elif users[1] != None:
                    Role = "Сотрудник"
                else:
                    Role = "Админ"
                break
            else:
                print("Логин или пароль не верен!")
                continue
        else:
            print("Повторите ввод логина и пароля: ")
            continue
    print("Успешный вход! ")

def Registration():
    while True:
        Name = input("Введите имя: ")
        Surname = input("Введите фамилию: ")
        Patronimic = input("Введите отчество")
        Loginn = input("Введите логин: ")
        password = input("Введите пароль: ")
        clean_Name = Name.strip()
        clean_Surname = Surname.strip()
        clean_Patronimic = Patronimic.strip()
        clean_login = Loginn.strip()
        clean_password = password.strip()
        if clean_login and clean_password and clean_Name and clean_Surname and clean_Patronimic:
            user = User(
                User_id = 0,
                name = clean_Name,
                surname = clean_Surname,
                patronymic = clean_Patronimic,
                loginn = clean_login,
                password = clean_password
            )
            data_base.Redistration_User(user)
            break
        else:
            print("Повторите ввод данных: ")
            continue
    print("Регистрация прошла успешно\n Войдите в систему:")
    login()