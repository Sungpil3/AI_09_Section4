# 유저 플레이기록을 db 에서 가져와서 dataframe으로 피클링
import psycopg2
import pickle
import pandas as pd
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

cur = connection.cursor()

cur.execute("SELECT * FROM user_date;")
rows = cur.fetchall()

data = []
for row in rows:
    data.append(row)

df = pd.DataFrame(data)
with open('data.pkl','wb') as pickle_file:
    pickle.dump(df, pickle_file)

print(df.head(2))

cur.close()
connection.close()    