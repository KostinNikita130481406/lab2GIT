from services import ServiceError
from repositories import client_repository, personal_repository, admin_repository

ROLE_CLIENT = "Клиент"
ROLE_PERSONAL = "Сотрудник"
ROLE_ADMIN = "Админ"


def _require(value, field_name):
    # Проверка: поле не пустое. Возвращает значение без лишних пробелов.
    value = (value or "").strip()
    if not value:
        raise ServiceError(f"Поле «{field_name}» не должно быть пустым")
    return value


def login_exists(login):
    # Логин должен быть уникальным среди клиентов, сотрудников и админов
    for repo in (client_repository, personal_repository, admin_repository):
        if any(str(user.Login) == login for user in repo.get_all()):
            return True
    return False


def login(login_text, password):
    # Возвращает (id пользователя, роль) или бросает ServiceError
    login_text = _require(login_text, "Логин")
    password = _require(password, "Пароль")
    variants = (
        (client_repository, ROLE_CLIENT, "Kod_client"),
        (personal_repository, ROLE_PERSONAL, "Kod_Personal"),
        (admin_repository, ROLE_ADMIN, "Kod_Admin"),
    )
    for repo, role, id_field in variants:
        for user in repo.get_all():
            # str(): столбцы объявлены как STRING, и SQLite хранит "123" числом
            if str(user.Login) == login_text and str(user.Password) == password:
                return getattr(user, id_field), role
    raise ServiceError("Логин или пароль не верен!")


def register_client(name, surname, patronymic, login_text, password):
    # Самостоятельно регистрируется только клиент
    name = _require(name, "Имя")
    surname = _require(surname, "Фамилия")
    patronymic = (patronymic or "").strip() or None   # отчество необязательно
    login_text = _require(login_text, "Логин")
    password = _require(password, "Пароль")
    if login_exists(login_text):
        raise ServiceError("Такой логин уже существует. Придумайте другой")
    client_repository.add(name, surname, patronymic, login_text, password)

def register_admin(name, surname, patronymic, login_text, password):
    name = _require(name, "Имя")
    surname = _require(surname, "Фамилия")
    patronymic = (patronymic or "").strip() or None  # отчество необязательно
    login_text = _require(login_text, "Логин")
    password = _require(password, "Пароль")
    if login_exists(login_text):
        raise ServiceError("Такой логин уже существует. Придумайте другой")
    admin_repository.add(name, surname, patronymic, login_text, password)
