from dataclasses import dataclass


@dataclass
class Client:
    Kod_client: int
    Name: str
    Surname: str
    Patronymic: str | None
    Login: str
    Password: str
