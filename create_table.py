# 유저 account_no를 수집할 table를 만든다
import psycopg2
host = 'localhost'
user = 'postgres'
password = '로컬 db 비밀번호'
database = 'kart4'

connection = psycopg2.connect(
    host=host,
    user=user,
    password=password,
    database=database
)
print(connection)

cur = connection.cursor()

table_name = 'user_account_no'
cur.execute(f"DROP TABLE IF EXISTS {table_name} CASCADE;")
cur.execute(f"""
CREATE TABLE {table_name} (
user_account_no INTEGER NOT NULL PRIMARY KEY
);"""
)

connection.commit()
cur.close()
connection.close()
