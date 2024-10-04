from psycopg2 import OperationalError, connect
from psycopg2.extensions import AsIs
from os import name

if name == 'posix':
    file_path = ''
    access_to_database = 'host all all all scram-sha-256\n'
 
    with open(file_path, 'a') as file:
        file.writelines(access_to_database)
        file.close()
elif name == 'nt':
    # pg_hba.conf
    file_path = ''
    access_to_database = 'host all all all scram-sha-256\n'
    # postgresql.conf
    file_path = ''
    listen_addresses = 'host all all all scram-sha-256\n'
    pass

# Параметры подключения к PostgreSQL
host = "localhost"
port = "5432"
user = "postgres"    # Пользователь с правами на создание других пользователей
password = "postgres"
dbname = "postgres"

# Новые данные для создания пользователя и базы данных
new_db_user = "test"
pass_for_new_user = "test"


try:
# Подключаемся к базе данных
    conn = connect(database=dbname, user=user, password=password, host=host, port=port)
    conn.autocommit = True
    cursor = conn.cursor()

    # Создание нового пользователя
    cursor.execute(f"CREATE USER %s WITH PASSWORD %s", (AsIs(new_db_user), pass_for_new_user))    
    print(f"Пользователь '{new_db_user}' успешно создан.")

except OperationalError as e:
    print(f"Ошибка: '{e}'")
finally:
    if conn:
        cursor.close()
        conn.close()
        print("Подключение к базе данных закрыто.")
