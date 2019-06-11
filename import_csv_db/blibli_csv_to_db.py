# -*- coding:utf-8 -*-
import pandas as pd
import psycopg2

conn = psycopg2.connect(database='spiders', user='postgres', password='123456',
                        host='127.0.0.1', port='5432')
cur = conn.cursor()
file_name = '6.5(2).csv'
df = pd.read_csv(file_name, encoding='gbk')

for index in df.index.tolist():
    row_data = df.loc[index].to_dict()
    cur.execute("""insert into data_blibli_download(video_id,video_title,video_url,type_name,cid,video_time,
    redis_task_id,is_download,add_time) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)""", (str(row_data['video_id']), str(row_data['video_title']),
    str(row_data['video_url']), str(row_data['type_name']), str(row_data['cid']), int(row_data['video_time']), None, False,
    str(row_data['add_time'])))
    conn.commit()

conn.close()