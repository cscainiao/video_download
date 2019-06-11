# -*- coding:utf-8 -*-
# des: import tasks to redis
import json

import redis
import psycopg2
from common import functions

redis_key = 'weibo_video_tasks'

# add_time = '2019-05-29'               # 添加任务到bd中的时间
REDIS_OBJ = redis.Redis()
conn = psycopg2.connect(database='spiders', user='postgres', password='123456',
                        host='127.0.0.1', port='5432')
cur = conn.cursor()


def run():
    time_now = functions.get_time_now()
    cur.execute("select video_id, video_url from weibo_video_info_download where is_download=False;")
    task_cfgs = cur.fetchall()
    for task_cfg in task_cfgs:
        video_id = task_cfg[0]
        url = task_cfg[1]
        cur.execute("update weibo_video_info_download set redis_task_id=%s where video_id=%s;", (time_now, video_id))
        conn.commit()
        REDIS_OBJ.lpush(redis_key, json.dumps({'video_id': video_id, 'url': url}))


def close():
    REDIS_OBJ.connection_pool.disconnect()
    conn.close()
    print('ok')


if __name__ == '__main__':
    run()
    close()
