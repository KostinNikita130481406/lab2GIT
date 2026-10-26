import menu
from services import ServiceError
from services.auth_service import login as auth_login, register_client


def open_menu(user_id, role):
    # Какое меню открыть, решает роль пользователя
    match role:
        case "Клиент":
            menu.menu_client(user_id)
        case "Сотрудник":
            menu.menu_master(user_id)
        case "Админ":
            menu.menu_admin(user_id)


def login():
    # Возвращает (id, роль) или None, если вход не удался
    login_text = input("Введите логин: ")
    password = input("Введите пароль: ")
    try:
        user_id, role = auth_login(login_text, password)
    except ServiceError as error:
        print(error)
        return None
    print("Успешный вход!")
    return user_id, role


def registration():
    # Возвращает True, если регистрация прошла
    print("Регистрация клиента")
    name = input("Введите имя: ")
    surname = input("Введите фамилию: ")
    patronymic = input("Введите отчество (можно пропустить): ")
    login_text = input("Введите логин: ")
    password = input("Введите пароль: ")
    try:
        register_client(name, surname, patronymic, login_text, password)
    except ServiceError as error:
        print(error)
        return False
    print("Регистрация прошла успешно. Войдите в систему.")
    return True


def registration_login():
    while True:
        print("\n1 - Войти в систему\n2 - Зарегистрироваться в системе\n0 - Выйти из программы")
        choice = input("Выберите пункт меню: ").strip()
        match choice:
            case "1":
                result = login()
                if result:
                    open_menu(*result)
            case "2":
                if registration():
                    result = login()
                    if result:
                        open_menu(*result)
            case "0":
                print("Программа закрыта")
                break
            case _:
                print("Нет такого пункта меню")
