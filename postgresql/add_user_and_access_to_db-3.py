from psycopg2 import OperationalError, connect
from psycopg2.extensions import AsIs
from os import name
import docker
from time import sleep
import subprocess


def check_host_all_line(file_path):
    try:
        with open(file_path, 'r') as file:
            for line in file:
                if "host all all all scram-sha-256" in line:
                    print("Found: host all all all scram-sha-256")
                    return True
            print("Not found: host all all all scram-sha-256")
            return False
    except FileNotFoundError:
        print("Error in block 'check_host_all_line'")
        print(f"File not found: {file_path}")
        return False

def check_listen_addresses(host, port, user, password, dbname):
    try:
        conn = connect(database=dbname, user=user, password=password, host=host, port=port)
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute("SHOW listen_addresses;")
        listen_addresses = cursor.fetchall()
        for i in listen_addresses:
            if '*' in i:
                print("Found: * for listen_addresses")
                return True
        print("Not found: * for listen_addresses")
        return False
    except FileNotFoundError:
        print("Error in block 'check_listen_addresses'")
        return False
    finally:
        if conn:
            cursor.close()
            conn.close()

def reload_pg_hba_conf(host, port, user, password, dbname):
    try:
        conn = connect(database=dbname, user=user, password=password, host=host, port=port)
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute("SELECT pg_reload_conf();")
        print("pg_hba.conf reload was successful")
    except Exception as e:
        print("Error in block 'reload_pg_hba_conf'")
        print(f'Error: {e}')
        return False
    finally:
        if conn:
            cursor.close()
            conn.close()
    return True

def reload_postgres_conf(service_name):
    if name == "posix":
        try:
            client = docker.from_env()
            container = client.containers.get(service_name)
            container.restart()
            sleep(5)
            print("postgresql.conf reload was successful")
        except Exception as e:
            print("Error in block 'reload_postgres_conf/posix")
            print(f'Error: {e}')
            return False 
    elif name == "nt":
        try:
            subprocess.run(['sc', 'stop', "IdMe-mas-meta-server-api"], check=True)
            sleep(5)
            subprocess.run(['sc', 'stop', "IdMe-mkv-server-auth"], check=True)
            sleep(5)
            subprocess.run(['sc', 'stop', service_name], check=True)
            sleep(5)
            subprocess.run(['sc', 'start', service_name], check=True)
            sleep(5)
            subprocess.run(['sc', 'start', "IdMe-mas-meta-server-api"], check=True)
            sleep(5)
            subprocess.run(['sc', 'start', "IdMe-mkv-server-auth"], check=True)
            sleep(5)
        except subprocess.CalledProcessError as e:
            print("Error in block 'reload_postgres_conf/nt'")
            print(f'Error: {e}')
            return False
    return True

def change_pg_hba(host, port, user, password, dbname):
    access_to_database = "host all all all scram-sha-256"

    if name == "posix":
        file_path_pg_hba = "/opt/recfaces/DATA/db/pg_hba.conf"
    elif name == "nt":
        file_path_pg_hba = r"C:\RECFACES\DATA\postgresql\pg_hba.conf"

    if not check_host_all_line(file_path_pg_hba):
        print("change pg_hba.conf configuration...")
        with open(file_path_pg_hba, "a") as file:
            if name == "posix":
                file.writelines(f"{access_to_database}\n")
            elif name == "nt":
                file.writelines(f"\n{access_to_database}\n")
        reload_pg_hba_conf(host, port, user, password, dbname)
        print("configuration changed successfully")
    else:
        print("pg_hba.conf access already exist!")
    return True

def change_postgresql_conf(host, port, user, password, dbname):
    if name == "posix":
        service_name = "Postgres"
        file_path_postgresql_conf = "/opt/recfaces/DATA/db/postgresql.conf"
    elif name == "nt":
        service_name = "PostgreSQL"
        file_path_postgresql_conf = r"C:\RECFACES\DATA\postgresql\postgresql.conf"

    if not check_listen_addresses(host, port, user, password, dbname):
        print("change postgresql.conf configuration...")
        try:
            conn = connect(database=dbname, user=user, password=password, host=host, port=port)
            conn.autocommit = True
            cursor = conn.cursor()
            cursor.execute("ALTER SYSTEM SET listen_addresses TO '*'")
            reload_postgres_conf(service_name)
            print("configuration changed successfully")
        except OperationalError as e:
            print("Error in block 'change_postgresql_conf/check_listen_addresses'")
            print(f"Error: '{e}'")
            return False 
        finally:
            if conn:
                cursor.close()
                conn.close()
    else:
        print("postgresql.conf access already exist!")
    return True

def create_db_user(host, port, user, password, dbname, new_db_user, pass_for_new_user):
    try:
        conn = connect(database=dbname, user=user, password=password, host=host, port=port)
        conn.autocommit = True
        cursor = conn.cursor()

        cursor.execute(f"CREATE USER %s WITH PASSWORD %s NOSUPERUSER CREATEDB NOCREATEROLE INHERIT LOGIN REPLICATION NOBYPASSRLS CONNECTION LIMIT -1;", (AsIs(new_db_user), pass_for_new_user))
        return True
    except OperationalError as e:
        print("Error in block 'create_db_user'")
        print(f"Error: '{e}'")
        return False
    finally:
        if conn:
            cursor.close()
            conn.close()
    return True

def main():
    host = "localhost"
    port = "5432"
    user = ""
    password = ""
    dbname = ""
    
    new_db_user = "test"
    pass_for_new_user = "test"

    if change_pg_hba(host, port, user, password, dbname):
        if change_postgresql_conf(host, port, user, password, dbname):
            print("access added successfully")
            if create_db_user(host, port, user, password, dbname, new_db_user, pass_for_new_user):
                print(f"the user has been successfully created.")


if __name__ == '__main__':
    main()
