from psycopg2 import OperationalError, connect
from psycopg2.extensions import AsIs
from os import name


if name == 'posix':
    file_path = ''
    access_to_database = 'host all all all scram-sha-256\n'
    
    with open(file_path, 'r') as file:
        text = file.read()
    
        if access_to_database not in text:
            with open(file_path, 'a') as file:
                file.writelines(access_to_database)
                file.close()

elif name == 'nt':
    # pg_hba.conf
    file_path = r'E:\\personal\\scripts\\postgresql\\pg_hba.conf'
    access_to_database = 'host all all all scram-sha-256\n'
    
    with open(file_path, 'r') as file:
        text = file.read()

        if access_to_database not in text:
            with open(file_path, 'a') as file:
                file.writelines(access_to_database)
                file.close()

    # postgresql.conf
    file_path = r'E:\\personal\\scripts\\postgresql\\postgresql.conf'
    listen_addresses = "listen_addresses = '*'\n"

    # Открытие файла для чтения
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Замена строки, содержащей часть текста
    for i, line in enumerate(lines):
        if 'listen_addresses' in line:
            lines[i] = listen_addresses

    # Запись изменённых строк обратно в файл
    with open(file_path, 'w') as file:
        file.writelines(lines)

# Параметры подключения к PostgreSQL
host = "10.0.0.30"
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
