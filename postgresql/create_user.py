from psycopg2 import OperationalError, connect
from psycopg2.extensions import AsIs
from os import name
import docker
from time import sleep


if name == 'posix':
    # Доступ к бд Linux
    file_path = '/opt/recfaces/DATA/db/pg_hba.conf'
    access_to_database = 'host all all all scram-sha-256\n'
    
    with open(file_path, 'r') as file:
        text = file.read()
    
        if access_to_database not in text:
            client = docker.from_env()
            container_name = 'Postgres'
            container = client.containers.get(container_name)
        
            with open(file_path, 'a') as file:
                file.writelines(access_to_database)
                file.close()

            container.restart()
            sleep(5)

elif name == 'nt':
    # Доступ к бд Windows
    file_path = r'E:\\personal\\scripts\\postgresql\\pg_hba.conf'
    access_to_database = 'host all all all scram-sha-256\n'
    
    with open(file_path, 'r') as file:
        text = file.read()

        if access_to_database not in text:
            with open(file_path, 'a') as file:
                file.writelines(access_to_database)
                file.close()

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
host = "localhost"
port = "5432"
user = "test1"    # Пользователь с правами на создание других пользователей
password = "test1"
dbname = "eosan"

# Новые данные для создания пользователя
new_db_user = "test"
pass_for_new_user = "test"


try:
# Подключаемся к базе данных
    conn = connect(database=dbname, user=user, password=password, host=host, port=port)
    conn.autocommit = True
    cursor = conn.cursor()

    # Создание нового пользователя
    cursor.execute(f"CREATE USER %s WITH PASSWORD %s SUPERUSER CREATEDB CREATEROLE LOGIN REPLICATION BYPASSRLS;", (AsIs(new_db_user), pass_for_new_user))    
    print(f"Пользователь '{new_db_user}' успешно создан.")

except OperationalError as e:
    print(f"Ошибка: '{e}'")
finally:
    if conn:
        cursor.close()
        conn.close()
        print("Подключение к базе данных закрыто.")
