from psycopg2 import OperationalError, connect
from psycopg2.extensions import AsIs
from os import name
import docker
from time import sleep
import re
import subprocess


def database_access():
    if name == "posix":
        # Доступ к бд Linux
        file_path = "/path/to/pg_hba.conf"
        access_to_database = "host all all all scram-sha-256\n"
        pattern = r"host all all all scram-sha-256"
        
        with open(file_path, "r") as file:
            text = file.read()
            search_access = re.search(pattern, text)
        
            if not search_access:
                print("Adding database access...")
                client = docker.from_env()
                container_name = "Postgres"
                container = client.containers.get(container_name)
            
                with open(file_path, "a") as file:
                    file.writelines(access_to_database)
                    file.close()

                container.restart()
                sleep(5)
            else:
                print("Database access already exist!")
                file.close()
                return False

            file.close()
            return True

    elif name == "nt":
        # Доступ к бд Windows
        file_path = r"C:\path\to\pg_hba.conf"
        access_to_database = "\nhost all all all scram-sha-256\n"
        pattern = r"host all all all scram-sha-256"
        
        with open(file_path, "r") as file:
            text = file.read()
            search_access = re.search(pattern, text)
        
            if not search_access:
                print("Adding database access...")
                service_name = 'postgresql-x64-14'
            
                with open(file_path, "a") as file:
                    file.writelines(access_to_database)
                    file.close()
                
                file_path = r'C:\path\to\postgresql.conf'
                listen_addresses = "listen_addresses = '*'\n"

                # Открытие файла для чтения
                with open(file_path, "r") as file:
                    lines = file.readlines()

                # Замена строки, содержащей часть текста
                for i, line in enumerate(lines):
                    if "listen_addresses" in line:
                        lines[i] = listen_addresses

                # Запись изменённых строк обратно в файл
                with open(file_path, "w") as file:
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
                file.close()
                return False

            file.close()
            return True

def create_db_user():
    # Параметры подключения к PostgreSQL
    host = "localhost"
    port = "5432"
    user = "postgres"    # Пользователь с правами на создание других пользователей
    password = "postgres"
    dbname = "postgres"

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
    if database_access():
        print("Access added successfully")

    if create_db_user():
        print(f"The user has been successfully created.")