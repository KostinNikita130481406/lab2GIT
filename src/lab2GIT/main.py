import data_base

# /////////////////////////////////////////////////////////////////////////////////////////////
print("Начало программы")
data_base.init_db()
while (True):
    print(" 1 - Завести клиента\n 2 - Завести сотрудника\n 3 - Завести заявку на ремонт\n 4 - Выйти из программы\n")
    choicee = int(input("Выберете вариант меню "))
    match choicee:
        case 1 :
            FULL_NAME = input("Введите ФИО клиента ")
            data_base.incert_client(FULL_NAME)
            data_base.Show_client()
        case 2:
            FULL_NAME = input("Введите ФИО сотрудника ")
            data_base.incert_personal(FULL_NAME)
            data_base.Show_personal()
        case 3:
            Data_income = input("Введите дату поступления заявки ")
            Type_electronics = input("Введите тип электротехники (Телефон, Телевизор, ПК и тд) ")
            Brand_name = input("Введите бренд техники (Bosh, LG, APPlE и тд ")
            Comment_problem = input("Введите описание проблемы с техникой ")
            print("Выберете клиента на которого будет назначена заявка ")
            data_base.Show_client()
            Kod_client = int(input())
            data_base.incert_application(Data_income,Type_electronics,Brand_name,Comment_problem,Kod_client)
            data_base.Show_application()
        case 4:
            print("Программа закрыта ")
            break




