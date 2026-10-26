from dataclasses import dataclass


@dataclass
class Admin:
    Kod_Admin: int
    Name: str
    Surname: str
    Patronymic: str | None
    Login: str
    Password: str
