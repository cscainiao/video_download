# -*- coding:utf-8 -*-

import os
import psycopg2

download_list = os.listdir('D:weibo_video')

conn = psycopg2.connect(database='spiders', user='postgres', password='123456',
                            host='127.0.0.1', port='5432')
cur = conn.cursor()

cur.execute("select video_id from weibo_video_info;")
data = cur.fetchall()
for each_data in data:
    video_id = each_data[0]
    if video_id not in download_list:
        cur.execute("delete from weibo_video_info where video_id=%s;",(video_id,))
        conn.commit()
conn.close()
print('ok')