import io
import os
import sqlite3
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src", "lab2GIT"))

import data_base
import repositories
import RegistrationLogin
from services import (AuthService, ApplicationService, StaffService,
                      ServiceError, ROLE_CLIENT, ROLE_PERSONAL, ROLE_ADMIN)


class BaseCase(unittest.TestCase):
    def setUp(self):
        # Для каждого теста своя временная база: настоящая service1 не затрагивается
        fd, self.path = tempfile.mkstemp(suffix=".db")
        os.close(fd)
        connect = lambda: sqlite3.connect(self.path)
        self._old = (data_base.get_connection, repositories.get_connection)
        data_base.get_connection = connect
        repositories.get_connection = connect
        data_base.init_db()
        self.clients = repositories.ClientRepository()
        self.personal = repositories.PersonalRepository()
        self.admins = repositories.AdminRepository()
        self.applications = repositories.ApplicationRepository()

    def tearDown(self):
        data_base.get_connection, repositories.get_connection = self._old
        os.remove(self.path)


class AuthTests(BaseCase):
    def test_register_and_login_client(self):
        auth = AuthService()
        auth.register_client("Иван", "Петров", "", "ivan", "123")
        user_id, role = auth.login("ivan", "123")
        self.assertEqual(role, ROLE_CLIENT)
        self.assertEqual(self.clients.get_by_id(user_id).Name, "Иван")
        self.assertIsNone(self.clients.get_by_id(user_id).Patronymic)

    def test_roles(self):
        self.personal.add("М", "М", None, "master", "1")
        self.admins.add("А", "А", None, "admin", "2")
        auth = AuthService()
        self.assertEqual(auth.login("master", "1")[1], ROLE_PERSONAL)
        self.assertEqual(auth.login("admin", "2")[1], ROLE_ADMIN)

    def test_wrong_password(self):
        auth = AuthService()
        auth.register_client("Иван", "Петров", "", "ivan", "123")
        with self.assertRaises(ServiceError):
            auth.login("ivan", "wrong")

    def test_duplicate_login_in_any_table(self):
        self.personal.add("М", "М", None, "master", "1")
        with self.assertRaises(ServiceError):
            AuthService().register_client("Иван", "Петров", "", "master", "123")

    def test_empty_fields(self):
        with self.assertRaises(ServiceError):
            AuthService().register_client("  ", "Петров", "", "x", "1")
        with self.assertRaises(ServiceError):
            AuthService().login("", "")


class ApplicationTests(BaseCase):
    def setUp(self):
        super().setUp()
        self.clients.add("Иван", "Петров", "Сергеевич", "c1", "1")
        self.clients.add("Олег", "Сидоров", None, "c2", "1")
        self.service = ApplicationService()

    def test_no_staff_application_unassigned(self):
        app = self.service.create(1, "Телефон", "LG", "не включается")
        self.assertIsNone(app.Kod_Personal)
        self.assertIsNone(app.Data_close)

    def test_auto_assignment_prefers_free_then_least_loaded(self):
        self.personal.add("А", "А", None, "m1", "1")
        self.personal.add("Б", "Б", None, "m2", "1")
        first = self.service.create(1, "Телефон", "LG", "x")
        second = self.service.create(1, "ТВ", "Sony", "y")
        self.assertEqual({first.Kod_Personal, second.Kod_Personal}, {1, 2})   # оба заняты по одной
        third = self.service.create(2, "ПК", "HP", "z")
        self.assertIn(third.Kod_Personal, (1, 2))
        # после закрытия сотрудник снова свободен и получает следующую заявку
        self.service.close(first.ID_Application, first.Kod_Personal)
        fourth = self.service.create(2, "Чайник", "Bosch", "w")
        self.assertEqual(fourth.Kod_Personal, first.Kod_Personal)

    def test_unassigned_applications_get_assigned_later(self):
        app = self.service.create(1, "Телефон", "LG", "x")     # сотрудников ещё нет
        self.assertIsNone(app.Kod_Personal)
        self.personal.add("А", "А", None, "m1", "1")
        self.assertEqual(self.service.assign_unassigned(), 1)
        self.assertEqual(self.service.get(app.ID_Application).Kod_Personal, 1)
        self.assertEqual(self.service.assign_unassigned(), 0)  # повторно ничего не делает

    def test_close_only_by_assigned(self):
        self.personal.add("А", "А", None, "m1", "1")
        self.personal.add("Б", "Б", None, "m2", "1")
        app = self.service.create(1, "Телефон", "LG", "x")
        other = 2 if app.Kod_Personal == 1 else 1
        with self.assertRaises(ServiceError):
            self.service.close(app.ID_Application, other)
        closed = self.service.close(app.ID_Application, app.Kod_Personal)
        self.assertIsNotNone(closed.Data_close)
        with self.assertRaises(ServiceError):
            self.service.close(app.ID_Application, app.Kod_Personal)

    def test_validation_and_missing_objects(self):
        with self.assertRaises(ServiceError):
            self.service.create(1, "Телефон", "LG", "   ")
        with self.assertRaises(ServiceError):
            self.service.create(99, "Телефон", "LG", "x")
        with self.assertRaises(ServiceError):
            self.service.get(12345)

    def test_client_edit_delete_only_own_open(self):
        app = self.service.create(1, "Телефон", "LG", "x")
        with self.assertRaises(ServiceError):
            self.service.update(app.ID_Application, 2, "ТВ", "Sony", "y")
        with self.assertRaises(ServiceError):
            self.service.delete(app.ID_Application, 2)
        changed = self.service.update(app.ID_Application, 1, "ТВ", "Sony", "нет звука")
        self.assertEqual(changed.Type_electronics, "ТВ")
        self.service.delete(app.ID_Application, 1)
        self.assertEqual(self.service.get_all(), [])

    def test_search_cyrillic_any_case(self):
        a = self.service.create(1, "Телефон", "LG", "x")
        b = self.service.create(2, "Телевизор", "Sony", "y")
        self.assertEqual([x.ID_Application for x in self.service.search_by_type("ТЕЛЕФ")], [a.ID_Application])
        self.assertEqual([x.ID_Application for x in self.service.search_by_client_name("сидоров")], [b.ID_Application])
        self.assertEqual([x.ID_Application for x in self.service.search_by_id(str(a.ID_Application))], [a.ID_Application])
        with self.assertRaises(ServiceError):
            self.service.search_by_id("abc")


class StaffTests(BaseCase):
    def test_add_and_delete(self):
        staff = StaffService()
        staff.add_personal("А", "А", "", "m1", "1")
        with self.assertRaises(ServiceError):
            staff.add_personal("Б", "Б", "", "m1", "2")       # логин занят
        self.clients.add("Иван", "Петров", None, "c1", "1")
        ApplicationService().create(1, "Телефон", "LG", "x")  # заявка назначена на сотрудника 1
        with self.assertRaises(ServiceError):
            staff.delete_personal(1)                           # есть заявки
        staff.add_personal("В", "В", "", "m2", "1")
        staff.delete_personal(2)
        self.assertEqual(len(staff.get_all()), 1)


class ScenarioTests(BaseCase):
    """Сквозная проверка: пользователь вводит данные в меню так, как это делали бы вы."""

    def run_program(self, answers):
        output = io.StringIO()
        with patch("builtins.input", side_effect=answers), redirect_stdout(output):
            RegistrationLogin.registration_login()
        return output.getvalue()

    def test_full_scenario(self):
        self.personal.add("Мастер", "Мастеров", None, "master", "m")
        self.admins.add("Админ", "Админов", None, "admin", "a")
        text = self.run_program([
            # регистрация клиента и вход, создание заявки, просмотр, пустое поле, выход
            "2", "Иван", "Петров", "", "ivan", "123",
            "ivan", "123",
            "1", "Телефон", "LG", "не включается",
            "1", "Телевизор", "Sony", "   ",
            "abc",
            "2",
            "0",
            # вход мастером: все заявки, закрыть свою, повторное закрытие, поиск, выход
            "1", "master", "m",
            "1",
            "5", "1",
            "5", "1",
            "4", "2", "петров",
            "0",
            # админ: список сотрудников, добавить, выход
            "1", "admin", "a",
            "1", "2", "Олег", "Сидоров", "", "oleg", "p", "1",
            "0",
            "0",
        ])
        for expected in ("Регистрация прошла успешно", "Заявка принята!", "не должно быть пустым",
                         "Введите число", "В работе", "Заявка закрыта", "Заявка уже закрыта",
                         "Заявка №1", "Сотрудник добавлен",
                         "oleg", "Программа закрыта"):
            self.assertIn(expected, text)
        self.assertEqual(len(self.personal.get_all()), 2)
        self.assertIsNotNone(self.applications.get_by_id(1).Data_close)


if __name__ == "__main__":
    unittest.main()
