from dataclasses import dataclass


@dataclass
class Personal:
    Kod_Personal: int
    Name: str
    Surname: str
    Patronymic: str | None
    Login: str
    Password: str
