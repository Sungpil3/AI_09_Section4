# 유저의 id를 api를 이용해서 db로 저장
import requests
import json
import os
import time
import datetime
import pickle
import psycopg2
host = 'localhost'
user = 'postgres'
password = '로컬 db 비밀번호'
database = 'kart4'
API_Key = 'open api key'
headers = {'Authorization': API_Key}
now = datetime.datetime(2022, 3, 17, 18, 35, 11)
for i in range(1, 363):
    start_date = str(now - datetime.timedelta(days=i))
    end_date= str(now - datetime.timedelta(days=i-1))
    url = 'https://api.nexon.co.kr/kart/v1.0/matches/all?start_date='+ start_date +'&end_date='+ end_date +'&offset=0&limit=200&match_types='
    time.sleep(0.1)
    json_data = requests.get(url, headers=headers)
    all_match_data = json.loads(json_data.text)
    if all_match_data['matches'] == None:
        print(f"{start_date} 부터 {end_date} 사이 에는 match data 가 없습니다.")
    else :
        match_id_list = []
        for ii in range(len(all_match_data['matches'])):
            match_id_list += all_match_data['matches'][ii]['matches']
        for count, match_id in enumerate(match_id_list) :
            print(f"{i}일 전의 {count}번째 match")
            url = 'https://api.nexon.co.kr/kart/v1.0/matches/'+ match_id
            time.sleep(0.2)
            json_data = requests.get(url, headers=headers)
            match_data = json.loads(json_data.text)
            if 'players' in match_data:
                for iii in range(len(match_data['players'])):
                    user_accNo = match_data['players'][iii]['accountNo']
                    try:
                        connection = psycopg2.connect(host=host,user=user,password=password,database=database)
                        cur = connection.cursor()
                        cur.execute(f"INSERT INTO user_account_no (user_account_no) VALUES ({int(user_accNo)});")
                        connection.commit()
                        cur.close()
                        connection.close()
                        print("user_id_추가완료")
                    except:
                        pass    
            else :
                try:
                    for teams in range(len(match_data['teams'])):
                        if match_data['teams'][teams]['players'] == None:
                            pass
                        else:    
                            for iii in range(len(match_data['teams'][teams]['players'])):                
                                user_accNo = match_data['teams'][teams]['players'][iii]['accountNo']
                                try:
                                    connection = psycopg2.connect(host=host,user=user,password=password,database=database)
                                    cur = connection.cursor()
                                    cur.execute(f"INSERT INTO user_account_no (user_account_no) VALUES ({int(user_accNo)});")
                                    connection.commit()
                                    cur.close()
                                    connection.close()
                                    print("user_id_추가완료")
                                except:
                                    pass
                except:
                    pass                