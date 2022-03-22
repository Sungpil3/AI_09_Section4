# 유저의 플레이 기록을 저장하는 table을 생성
import time
import datetime
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
now = datetime.datetime(2022, 3, 17, 18, 35, 11)
date_list = []
for i in range(365, -1, -1):
    date_list.append(f"d{i}")
cur = connection.cursor()
table_name = 'user_date'
cur.execute(f"DROP TABLE IF EXISTS {table_name} CASCADE;")
cur.execute(f"""
CREATE TABLE {table_name} (
user_account_no INTEGER NOT NULL PRIMARY KEY,
{",".join([f"{i} INTEGER" for i in date_list])}
);"""
)

connection.commit()
cur.close()
connection.close()


