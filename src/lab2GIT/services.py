from datetime import date

from repositories import (ClientRepository, PersonalRepository,
                          AdminRepository, ApplicationRepository)

ROLE_CLIENT = "Клиент"
ROLE_PERSONAL = "Сотрудник"
ROLE_ADMIN = "Админ"


class ServiceError(Exception):
    """Ошибка бизнес-логики. Её текст можно показывать пользователю."""


def _require(value, field_name):
    # Проверка: поле не пустое. Возвращает значение без лишних пробелов.
    value = (value or "").strip()
    if not value:
        raise ServiceError(f"Поле «{field_name}» не должно быть пустым")
    return value


class AuthService:
    """Вход и регистрация."""

    def __init__(self):
        self.clients = ClientRepository()
        self.personal = PersonalRepository()
        self.admins = AdminRepository()

    def login_exists(self, login):
        # Логин должен быть уникальным среди клиентов, сотрудников и админов
        for repo in (self.clients, self.personal, self.admins):
            if any(str(user.Login) == login for user in repo.get_all()):
                return True
        return False

    def login(self, login, password):
        # Возвращает (id пользователя, роль) или бросает ServiceError
        login = _require(login, "Логин")
        password = _require(password, "Пароль")
        variants = (
            (self.clients, ROLE_CLIENT, "Kod_client"),
            (self.personal, ROLE_PERSONAL, "Kod_Personal"),
            (self.admins, ROLE_ADMIN, "Kod_Admin"),
        )
        for repo, role, id_field in variants:
            for user in repo.get_all():
                # str(): столбцы объявлены как STRING, и SQLite хранит "123" числом
                if str(user.Login) == login and str(user.Password) == password:
                    return getattr(user, id_field), role
        raise ServiceError("Логин или пароль не верен!")

    def register_client(self, name, surname, patronymic, login, password):
        # Самостоятельно регистрируется только клиент
        name = _require(name, "Имя")
        surname = _require(surname, "Фамилия")
        patronymic = (patronymic or "").strip() or None   # отчество необязательно
        login = _require(login, "Логин")
        password = _require(password, "Пароль")
        if self.login_exists(login):
            raise ServiceError("Такой логин уже существует. Придумайте другой")
        self.clients.add(name, surname, patronymic, login, password)


class ApplicationService:
    """Заявки: создание, автоназначение сотрудника, закрытие, поиск."""

    def __init__(self):
        self.applications = ApplicationRepository()
        self.clients = ClientRepository()
        self.personal = PersonalRepository()

    def _choose_personal(self):
        # Свободный сотрудник (0 открытых заявок) или тот, у кого их меньше всего.
        # При равенстве берём сотрудника с меньшим номером.
        staff = self.personal.get_all()
        if not staff:
            return None
        best = min(staff, key=lambda p: (
            self.applications.count_open_by_personal(p.Kod_Personal), p.Kod_Personal))
        return best.Kod_Personal

    def create(self, kod_client, type_electronics, brand_name, comment_problem):
        type_electronics = _require(type_electronics, "Тип техники")
        brand_name = _require(brand_name, "Бренд")
        comment_problem = _require(comment_problem, "Описание неисправности")
        if self.clients.get_by_id(kod_client) is None:
            raise ServiceError("Клиент не найден")
        kod_personal = self._choose_personal()
        new_id = self.applications.add(str(date.today()), type_electronics, brand_name,
                                       comment_problem, kod_client, kod_personal)
        return self.applications.get_by_id(new_id)

    def assign_unassigned(self):
        # Заявки без исполнителя (например, созданные, когда не было сотрудников)
        # получают сотрудника по тому же правилу. Возвращает число назначенных.
        assigned = 0
        for application in self.applications.get_all():
            if application.Kod_Personal is None and application.Data_close is None:
                kod_personal = self._choose_personal()
                if kod_personal is None:
                    break
                self.applications.assign(application.ID_Application, kod_personal)
                assigned += 1
        return assigned

    def get(self, id_application):
        application = self.applications.get_by_id(id_application)
        if application is None:
            raise ServiceError(f"Заявка №{id_application} не найдена")
        return application

    def get_all(self):
        return self.applications.get_all()

    def get_by_client(self, kod_client):
        return self.applications.get_by_client(kod_client)

    def get_by_personal(self, kod_personal):
        return self.applications.get_by_personal(kod_personal)

    def close(self, id_application, kod_personal):
        # Закрыть заявку может только тот сотрудник, которому она назначена
        application = self.get(id_application)
        if application.Data_close is not None:
            raise ServiceError("Заявка уже закрыта")
        if application.Kod_Personal != kod_personal:
            raise ServiceError("Закрыть заявку может только назначенный на неё сотрудник")
        self.applications.close(id_application, str(date.today()))
        return self.get(id_application)

    def _own_open_application(self, id_application, kod_client):
        application = self.get(id_application)
        if application.Kod_client != kod_client:
            raise ServiceError("Это не ваша заявка")
        if application.Data_close is not None:
            raise ServiceError("Закрытую заявку нельзя изменять и удалять")
        return application

    def update(self, id_application, kod_client, type_electronics, brand_name, comment_problem):
        self._own_open_application(id_application, kod_client)
        type_electronics = _require(type_electronics, "Тип техники")
        brand_name = _require(brand_name, "Бренд")
        comment_problem = _require(comment_problem, "Описание неисправности")
        self.applications.update(id_application, type_electronics, brand_name, comment_problem)
        return self.get(id_application)

    def delete(self, id_application, kod_client):
        self._own_open_application(id_application, kod_client)
        self.applications.delete(id_application)

    def search_by_id(self, text):
        try:
            id_application = int(text)
        except ValueError:
            raise ServiceError("Номер заявки должен быть числом")
        application = self.applications.get_by_id(id_application)
        return [application] if application else []

    def search_by_client_name(self, text):
        return self.applications.search_by_client_name(_require(text, "ФИО клиента"))

    def search_by_type(self, text):
        return self.applications.search_by_type(_require(text, "Вид техники"))


class StaffService:
    """Управление сотрудниками (для администратора)."""

    def __init__(self):
        self.personal = PersonalRepository()
        self.applications = ApplicationRepository()
        self.auth = AuthService()

    def get_all(self):
        return self.personal.get_all()

    def add_personal(self, name, surname, patronymic, login, password):
        name = _require(name, "Имя")
        surname = _require(surname, "Фамилия")
        patronymic = (patronymic or "").strip() or None
        login = _require(login, "Логин")
        password = _require(password, "Пароль")
        if self.auth.login_exists(login):
            raise ServiceError("Такой логин уже существует")
        self.personal.add(name, surname, patronymic, login, password)

    def delete_personal(self, kod_personal):
        if self.personal.get_by_id(kod_personal) is None:
            raise ServiceError("Сотрудник не найден")
        if self.applications.get_by_personal(kod_personal):
            raise ServiceError("К сотруднику привязаны заявки, удалить его нельзя")
        self.personal.delete(kod_personal)
