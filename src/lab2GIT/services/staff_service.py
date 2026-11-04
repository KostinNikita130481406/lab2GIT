from services import ServiceError
from services.auth_service import _require, login_exists
from repositories import personal_repository, application_repository
from services import security


def get_all():
    return personal_repository.get_all()


def add_personal(name, surname, patronymic, login_text, password):
    name = _require(name, "Имя")
    surname = _require(surname, "Фамилия")
    patronymic = (patronymic or "").strip() or None
    login_text = _require(login_text, "Логин")
    password = _require(password, "Пароль")
    if login_exists(login_text):
        raise ServiceError("Такой логин уже существует")
    personal_repository.add(name, surname, patronymic, login_text, security.hash_password(password))


def delete_personal(kod_personal):
    if personal_repository.get_by_id(kod_personal) is None:
        raise ServiceError("Сотрудник не найден")
    if application_repository.get_by_personal(kod_personal):
        raise ServiceError("К сотруднику привязаны заявки, удалить его нельзя")
    personal_repository.delete(kod_personal)
