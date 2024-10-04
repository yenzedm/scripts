import psycopg2
from psycopg2 import sql

# Параметры подключения к PostgreSQL
host = "10.0.0.30"
port = "5432"
user = "postgres"    # Пользователь с правами на создание других пользователей/баз
password = "postgres"
dbname = "postgres"

# Новые данные для создания пользователя и базы данных
new_db_user = "test"

# Подключение к PostgreSQL
try:
    # Подключаемся к базе данных
    conn = psycopg2.connect(host=host, dbname=dbname, user=user, password=password, port=port)
    conn.autocommit = True  # Устанавливаем автокоммит для создания пользователя/базы
    cursor = conn.cursor()

#    # Создание нового пользователя
#    create_user_query = sql.SQL("CREATE USER {} WITH PASSWORD %s").format(sql.Identifier(new_db_user))
#    cursor.execute(create_user_query, [new_db_password])
#    print(f"Пользователь '{new_db_user}' успешно создан.")
#
#    # Назначение прав новому пользователю на созданную базу данных
#    grant_privileges_query = sql.SQL("GRANT ALL PRIVILEGES ON DATABASE {} TO {}").format(
#        sql.Identifier(new_db_name), sql.Identifier(new_db_user)
#    )
#    cursor.execute(grant_privileges_query)
#    print(f"Пользователю '{new_db_user}' даны права на базу данных '{new_db_name}'.")

except Exception as e:
    print(f"Ошибка: {e}")
finally:
    if conn:
        cursor.close()
        conn.close()
        print("Подключение к базе данных закрыто.")
