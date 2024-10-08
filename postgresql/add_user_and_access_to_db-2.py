from psycopg2 import OperationalError, connect
from psycopg2.extensions import AsIs
from os import name
import docker
from time import sleep
import re
import subprocess

# linux
file_path_pg_hba_lin = "/path/to/pg_hba.conf"
access_to_database_lin = "host all all all scram-sha-256\n"
container_name = "Postgres"

# windows
file_path_pg_hba_win = r"C:\path\to\pg_hba.conf"
file_path_postgresql_conf_win = r"C:\path\to\postgresql.conf"
service_name = 'postgresql-x64-14'
change_listen_addresses = "listen_addresses = '*'\n"
access_to_database_win = "\nhost all all all scram-sha-256\n"

# linux and windows
pattern_for_search_access = r"host all all all scram-sha-256"

# Параметры подключения к PostgreSQL
host = "localhost"
port = "5432"
user = "postgres"    # Пользователь с правами на создание других пользователей
password = "postgres"
dbname = "postgres"

# Новые данные для создания пользователя
new_db_user = "test"
pass_for_new_user = "test"

def database_access_lin(file_path_pg_hba_lin, access_to_database_lin, container_name, pattern_for_search_access):
    with open(file_path_pg_hba_lin, "r") as file:
            text = file.read()
            search_access = re.search(pattern_for_search_access, text)

            # Если доступ уже будет в конце конфига, то Галя у нас отмена
            if not search_access:
                print("Adding database access...")
                client = docker.from_env()
                container = client.containers.get(container_name)

                # pg_hba.conf
                # Добавить в конец файла access_to_database
                with open(file_path_pg_hba_lin, "a") as file:
                    file.writelines(access_to_database_lin)

                container.restart()
                sleep(5)
            else:
                print("Database access already exist!")
                return False
            return True

def database_access_win(file_path_pg_hba_win, file_path_postgresql_conf_win, service_name, change_listen_addresses, pattern_for_search_access, access_to_database_win):
    with open(file_path_pg_hba_win, "r") as file:
        text = file.read()
        search_access = re.search(pattern_for_search_access, text)
    
        if not search_access:
            print("Adding database access...")
            
            # pg_hba.conf
            # Добавить в конец файла access_to_database
            with open(file_path_pg_hba_win, "a") as file:
                file.writelines(access_to_database_win)

            # postgresql.conf
            # Открытие файла для чтения
            with open(file_path_postgresql_conf_win, "r") as file:
                lines = file.readlines()

            # Замена строки, содержащей часть текста
            for i, line in enumerate(lines):
                if "listen_addresses" in line:
                    lines[i] = change_listen_addresses

            # Запись изменённых строк обратно в файл
            with open(file_path_postgresql_conf_win, "w") as file:
                file.writelines(lines)
            
            try:
                subprocess.run(['sc', 'stop', service_name], check=True)
                sleep(3)
                subprocess.run(['sc', 'start', service_name], check=True)
                sleep(3)
            except subprocess.CalledProcessError as e:
                print(f'Error: {e}')
        else:
            print("Database access already exist!")
            return False
        return True

def create_db_user(host, port, user, password, dbname, new_db_user, pass_for_new_user):
    try:
    # Подключаемся к базе данных
        conn = connect(database=dbname, user=user, password=password, host=host, port=port)
        conn.autocommit = True
        cursor = conn.cursor()

        # Создание нового пользователя
        cursor.execute(f"CREATE USER %s WITH PASSWORD %s SUPERUSER CREATEDB CREATEROLE LOGIN REPLICATION BYPASSRLS;", (AsIs(new_db_user), pass_for_new_user))
        return True

    except OperationalError as e:
        print(f"Error: '{e}'")
        return False

    finally:
        if conn:
            cursor.close()
            conn.close()
            print("The database connection is closed.")


if __name__ == '__main__':

    if name == "posix":
        if database_access_lin(file_path_pg_hba_lin, access_to_database_lin, container_name, pattern_for_search_access):
            print("Access added successfully")
    elif name == "nt":
        if database_access_win(file_path_pg_hba_win, file_path_postgresql_conf_win, service_name, change_listen_addresses, pattern_for_search_access, access_to_database_win):
            print("Access added successfully")
    
    if create_db_user(host, port, user, password, dbname, new_db_user, pass_for_new_user):
            print(f"The user has been successfully created.")