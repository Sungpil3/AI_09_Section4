# 유저의 플레이 기록을 db로 저장
import requests
import json
import os
import time
import datetime
import pickle
import psycopg2
from collections import Counter
import random
API_Key = 'open api key'
headers = {'Authorization': API_Key}
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

cur.execute("SELECT * FROM user_account_no;")
rows = cur.fetchall()
user_account_no_list = []
for row in rows:
    user_account_no_list.append(row[0])            
cur.close()
connection.close()
random.shuffle(user_account_no_list)
for count, user_account_no in enumerate(user_account_no_list):
    try:
        now = datetime.datetime(2022, 3, 17, 18, 35, 11)
        start_date = str(now - datetime.timedelta(days=365))
        end_date= str(now - datetime.timedelta(days=1-1))
        url = f"https://api.nexon.co.kr/kart/v1.0/users/{user_account_no}/matches?start_date={start_date}&end_date={end_date}&offset=0&limit=200"
        time.sleep(0.2)
        json_data = requests.get(url, headers=headers)
        print("첫 requests 완료")
        all_match_data = json.loads(json_data.text)
        all_match_time_list = []
        match_time_list = []
        for i in all_match_data["matches"]:
            for ii in i["matches"]:
                match_time_list.append((now - datetime.datetime.strptime(ii["startTime"], "%Y-%m-%dT%H:%M:%S")).days)
        all_match_time_list += match_time_list
        start_date = str(now - datetime.timedelta(days=365))
        end_date= str(now - datetime.timedelta(days=max(match_time_list)))        
        while True:
            url = f"https://api.nexon.co.kr/kart/v1.0/users/{user_account_no}/matches?start_date={start_date}&end_date={end_date}&offset=0&limit=200"
            time.sleep(0.2)
            json_data = requests.get(url, headers=headers)
            print("while문 내의 requests 완료")
            all_match_data = json.loads(json_data.text)
            if len(all_match_data["matches"]) == 0:
                print("while문 탈출")
                break
            else:
                match_time_list = []
                for i in all_match_data["matches"]:
                    for ii in i["matches"]:
                        match_time_list.append((now - datetime.datetime.strptime(ii["startTime"], "%Y-%m-%dT%H:%M:%S")).days)
                all_match_time_list += match_time_list        
                start_date = str(now - datetime.timedelta(days=365))
                end_date= str(now - datetime.timedelta(days=max(match_time_list)+1))
        result = Counter(all_match_time_list)
        user_play_date_dict = dict(result)
        connection = psycopg2.connect(host=host,user=user,password=password,database=database)
        cur = connection.cursor()
        cur.execute(f"""INSERT INTO user_date (user_account_no, {",".join([f"d{i}" for i in list(user_play_date_dict.keys())])}) VALUES ({user_account_no}, {",".join([f"{i}" for i in list(user_play_date_dict.values())])});""")
        connection.commit()
        cur.close()
        connection.close()
        print(f"{count}번째 인원 데이터 추가 완료")
    except:
        print(f"{count}번째 인원 실패")        