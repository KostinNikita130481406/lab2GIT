from repositories import application_repository
from repositories.application_repository import get_ALL_by_unload


def unload_menu():
    print("1 - .json\n2 - .csv\n3 - .xml\n4 - .yaml\n5 - вернуться в главное меню")
    choose = int(input('выберете вариант выгрузки данных'))
    match choose:
        case 1:
            unload_menu()
        case 2:
            unload_CSV()
        case 3:
            unload_XML()
        case 4:
            unload_YAML()
        case 5:
            pass
        case _:
            print("Такого варианта нету: ")




def unload_XML():
    get_ALL_by_unload()
    pass

def unload_JSON():
    pass

def unload_CSV():
    pass

def unload_YAML():
    pass