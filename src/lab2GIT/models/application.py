from dataclasses import dataclass


@dataclass
class Application:
    ID_Application: int
    Data_income: str
    Type_electronics: str
    Brand_name: str
    Comment_problem: str
    Data_close: str | None
    Kod_client: int
    Kod_Personal: int | None
