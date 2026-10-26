from datetime import date

from services import ServiceError
from services.auth_service import _require
from repositories import client_repository, personal_repository, application_repository


def _choose_personal():
    # Свободный сотрудник (0 открытых заявок) или тот, у кого их меньше всего.
    # При равенстве берём сотрудника с меньшим номером.
    staff = personal_repository.get_all()
    if not staff:
        return None
    best = min(staff, key=lambda p: (
        application_repository.count_open_by_personal(p.Kod_Personal), p.Kod_Personal))
    return best.Kod_Personal


def create(kod_client, type_electronics, brand_name, comment_problem):
    type_electronics = _require(type_electronics, "Тип техники")
    brand_name = _require(brand_name, "Бренд")
    comment_problem = _require(comment_problem, "Описание неисправности")
    if client_repository.get_by_id(kod_client) is None:
        raise ServiceError("Клиент не найден")
    kod_personal = _choose_personal()
    new_id = application_repository.add(str(date.today()), type_electronics, brand_name,
                                        comment_problem, kod_client, kod_personal)
    return application_repository.get_by_id(new_id)


def assign_unassigned():
    # Заявки без исполнителя (например, созданные, когда не было сотрудников)
    # получают сотрудника по тому же правилу. Возвращает число назначенных.
    assigned = 0
    for application in application_repository.get_all():
        if application.Kod_Personal is None and application.Data_close is None:
            kod_personal = _choose_personal()
            if kod_personal is None:
                break
            application_repository.assign(application.ID_Application, kod_personal)
            assigned += 1
    return assigned


def get(id_application):
    application = application_repository.get_by_id(id_application)
    if application is None:
        raise ServiceError(f"Заявка №{id_application} не найдена")
    return application


def get_all():
    return application_repository.get_all()


def get_by_client(kod_client):
    return application_repository.get_by_client(kod_client)


def get_by_personal(kod_personal):
    return application_repository.get_by_personal(kod_personal)


def close(id_application, kod_personal):
    # Закрыть заявку может только тот сотрудник, которому она назначена
    application = get(id_application)
    if application.Data_close is not None:
        raise ServiceError("Заявка уже закрыта")
    if application.Kod_Personal != kod_personal:
        raise ServiceError("Закрыть заявку может только назначенный на неё сотрудник")
    application_repository.close(id_application, str(date.today()))
    return get(id_application)


def _own_open_application(id_application, kod_client):
    application = get(id_application)
    if application.Kod_client != kod_client:
        raise ServiceError("Это не ваша заявка")
    if application.Data_close is not None:
        raise ServiceError("Закрытую заявку нельзя изменять и удалять")
    return application


def update(id_application, kod_client, type_electronics, brand_name, comment_problem):
    _own_open_application(id_application, kod_client)
    type_electronics = _require(type_electronics, "Тип техники")
    brand_name = _require(brand_name, "Бренд")
    comment_problem = _require(comment_problem, "Описание неисправности")
    application_repository.update(id_application, type_electronics, brand_name, comment_problem)
    return get(id_application)


def delete(id_application, kod_client):
    _own_open_application(id_application, kod_client)
    application_repository.delete(id_application)


def search_by_id(text):
    try:
        id_application = int(text)
    except ValueError:
        raise ServiceError("Номер заявки должен быть числом")
    application = application_repository.get_by_id(id_application)
    return [application] if application else []


def search_by_client_name(text):
    return application_repository.search_by_client_name(_require(text, "ФИО клиента"))


def search_by_type(text):
    return application_repository.search_by_type(_require(text, "Вид техники"))
