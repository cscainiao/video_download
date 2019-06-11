# -*- coding:utf-8 -*-
import psycopg2

from download.bilibili_video_download_fail_deal import download_file
from common.functions import rm_video
import os
base_dir = 'D:\Blibli_video'
fail_list = ['24160893',]

def run():
    conn = psycopg2.connect(database='spiders', user='postgres', password='123456',
                            host='127.0.0.1', port='5432')
    cur = conn.cursor()
    for video_id in fail_list:
        rm_video(video_id)
        cur.execute("select cid from data_blibli_download where video_id=%s;",(video_id,))
        cid = cur.fetchone()[0]
        download_file(video_id, cid)
    conn.close()


if __name__ == '__main__':
    run()