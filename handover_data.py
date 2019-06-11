# -*- coding:utf-8 -*-
import psycopg2

conn = psycopg2.connect(database='spiders', user='postgres', password='123456',
                            host='127.0.0.1', port='5432')
cur = conn.cursor()

cur.execute("select video_id from data_blibli_handover;")

data = cur.fetchall()
for each_data in data:
    video_id = each_data[0]
    qiniu_url = 'http://video.meb.com/' + str(video_id) + '-t.mp4'
    cur.execute("update data_blibli_handover set qiniu_url=%s where video_id=%s;", (qiniu_url,video_id))
    conn.commit()
conn.close()