import ctypes
import json
import os
import platform
import time

import psycopg2
import redis


def get_free_space_mb(folder='D:\\'):
  if platform.system() == 'Windows':
    free_bytes = ctypes.c_ulonglong(0)
    ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(folder), None, None, ctypes.pointer(free_bytes))
    return free_bytes.value/1024/1024/1024
  else:
    st = os.statvfs(folder)
    return st.f_bavail * st.f_frsize/1024/1024


def get_time_now():
    """
    获取当前时间
    """
    loc_time = time.localtime(time.time())
    time_now = time.strftime('%Y-%m-%d %H:%M:%S', loc_time)
    return time_now


def update_is_download(video_id, tb_name):
    conn = psycopg2.connect(database='spiders', user='postgres', password='123456',
                            host='127.0.0.1', port='5432')
    cur = conn.cursor()
    if 'blibli' in tb_name:
        cur.execute("update data_blibli_download set is_download=true where video_id=%s;", (video_id,))
    elif 'onetake' in tb_name:
        cur.execute("update data_onetake_download set is_download=true where video_id=%s;", (video_id,))
    elif 'vue' in tb_name:
        cur.execute("update data_vue_download set is_download=true where video_id=%s;", (video_id,))
    conn.commit()
    conn.close()


def rm_video(video_id):
    video_id = str(video_id)
    base_dir = 'D:\Blibli_video'
    try:
        for file_name in os.listdir(os.path.join(base_dir, video_id)):
            os.remove(os.path.join(base_dir, video_id, file_name))
        os.rmdir(os.path.join(base_dir, video_id))
    except:
        pass


def load_task(task_num, redis_key):
    REDIS_OBJ = redis.Redis()
    len_tasks = REDIS_OBJ.llen(redis_key)
    if len_tasks >= task_num:
        key_list = REDIS_OBJ.lrange(redis_key, 1, task_num)
        task_list = [json.loads(key) for key in key_list]
        REDIS_OBJ.ltrim(redis_key, task_num, -1)
        REDIS_OBJ.connection_pool.disconnect()
        return task_list
    elif len_tasks > 0:
        key_list = REDIS_OBJ.lrange(redis_key, 0, len_tasks)
        task_list = [json.loads(key) for key in key_list]
        REDIS_OBJ.ltrim(redis_key, len_tasks, -1)
        REDIS_OBJ.connection_pool.disconnect()
        return task_list
    else:
        REDIS_OBJ.connection_pool.disconnect()
        return []


def get_ip():
    """
    获取代理ip
    """
    r = redis.Redis()

    ip_b = r.rpop('weibo_proxies_queue')
    if not ip_b:
        return None
    ip_s = str(ip_b, 'utf-8')
    r.lpush('weibo_proxies_queue', ip_s)
    r.connection_pool.disconnect()
    return ip_s


def get_ip_api():
    import requests
    url = 'http://api.wandoudl.com/api/ip?app_key=7aaabcc48e4bbf7586848b9b417bec96&pack=2&num=1&xy=1&type=2&lb=\r\n&mr=1'
    res = requests.get(url)
    if res.status_code == 200:
        res_json = res.json()
        data = res_json['data'][0]
        ip = data['ip']
        port = data['port']
        proxie = str(ip) + ':' + str(port)
        return proxie
    else:return None

