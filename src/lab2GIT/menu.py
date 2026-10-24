from services import ApplicationService, StaffService, ServiceError


def ask_number(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Введите число")


def show_application(application):
    status = "В работе" if application.Data_close is None else f"закрыта {application.Data_close}"
    if application.Kod_Personal is None:
        executor = "не назначен"
    else:
        executor = f"сотрудник №{application.Kod_Personal}"
    print(f"Заявка №{application.ID_Application} от {application.Data_income}: "
          f"{application.Type_electronics}, {application.Brand_name}, "
          f"проблема: {application.Comment_problem}. "
          f"Клиент №{application.Kod_client}, исполнитель: {executor}. Статус: {status}")


def show_list(applications, empty_text="Заявок нет"):
    if not applications:
        print(empty_text)
        return
    for application in applications:
        show_application(application)


def menu_client(user_id):
    service = ApplicationService()
    while True:
        print("\nМЕНЮ КЛИЕНТА\n1 - Создать новую заявку\n2 - Мои заявки\n"
              "3 - Изменить заявку\n4 - Удалить заявку\n0 - Выход")
        choice = ask_number("Ваш выбор: ")
        try:
            match choice:
                case 1:
                    type_electronics = input("Тип техники (Телефон, Телевизор, ПК и т.д.): ")
                    brand_name = input("Бренд: ")
                    comment_problem = input("Что не так с техникой: ")
                    application = service.create(user_id, type_electronics, brand_name, comment_problem)
                    print("Заявка принята!")
                    show_application(application)
                case 2:
                    show_list(service.get_by_client(user_id), "У вас пока нет заявок")
                case 3:
                    id_application = ask_number("Номер заявки: ")
                    type_electronics = input("Новый тип техники: ")
                    brand_name = input("Новый бренд: ")
                    comment_problem = input("Новое описание неисправности: ")
                    service.update(id_application, user_id, type_electronics, brand_name, comment_problem)
                    print("Заявка изменена")
                case 4:
                    service.delete(ask_number("Номер заявки: "), user_id)
                    print("Заявка удалена")
                case 0:
                    break
                case _:
                    print("Нет такого пункта меню")
        except ServiceError as error:
            print(error)


def search_applications(service):
    print("Искать по: 1 - номеру заявки, 2 - ФИО клиента, 3 - виду техники")
    kind = ask_number("Ваш выбор: ")
    if kind not in (1, 2, 3):
        print("Нет такого варианта")
        return
    text = input("Что искать: ")
    match kind:
        case 1:
            result = service.search_by_id(text)
        case 2:
            result = service.search_by_client_name(text)
        case 3:
            result = service.search_by_type(text)
    show_list(result, "Ничего не найдено")


def menu_master(user_id):
    service = ApplicationService()
    assigned = service.assign_unassigned()
    if assigned:
        print(f"Заявок без исполнителя распределено между сотрудниками: {assigned}")
    while True:
        print("\nМЕНЮ СОТРУДНИКА\n1 - Список всех заявок\n2 - Мои заявки\n"
              "3 - Просмотр заявки\n4 - Найти заявку\n5 - Закрыть заявку\n0 - Выход")
        choice = ask_number("Ваш выбор: ")
        try:
            match choice:
                case 1:
                    show_list(service.get_all())
                case 2:
                    show_list(service.get_by_personal(user_id), "За вами пока нет заявок")
                case 3:
                    show_application(service.get(ask_number("Номер заявки: ")))
                case 4:
                    search_applications(service)
                case 5:
                    application = service.close(ask_number("Номер заявки для закрытия: "), user_id)
                    print("Заявка закрыта")
                    show_application(application)
                case 0:
                    break
                case _:
                    print("Нет такого пункта меню")
        except ServiceError as error:
            print(error)


def menu_admin(user_id):
    staff_service = StaffService()
    application_service = ApplicationService()
    while True:
        print("\nМЕНЮ АДМИНИСТРАТОРА\n1 - Список сотрудников\n2 - Добавить сотрудника\n"
              "3 - Удалить сотрудника\n4 - Все заявки\n0 - Выход")
        choice = ask_number("Ваш выбор: ")
        try:
            match choice:
                case 1:
                    staff = staff_service.get_all()
                    if not staff:
                        print("Сотрудников нет")
                    for person in staff:
                        print(f"№{person.Kod_Personal} {person.Surname} {person.Name} "
                              f"{person.Patronymic or ''} (логин {person.Login})")
                case 2:
                    name = input("Имя: ")
                    surname = input("Фамилия: ")
                    patronymic = input("Отчество (можно пропустить): ")
                    login = input("Логин: ")
                    password = input("Пароль: ")
                    staff_service.add_personal(name, surname, patronymic, login, password)
                    print("Сотрудник добавлен")
                case 3:
                    staff_service.delete_personal(ask_number("Номер сотрудника: "))
                    print("Сотрудник удалён")
                case 4:
                    show_list(application_service.get_all())
                case 0:
                    break
                case _:
                    print("Нет такого пункта меню")
        except ServiceError as error:
            print(error)
