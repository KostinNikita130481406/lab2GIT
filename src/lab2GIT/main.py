from database.database import init_db
import RegistrationLogin

# /////////////////////////////////////////////////////////////////////////////////////////////
print("Начало программы")
init_db()
RegistrationLogin.registration_login()
