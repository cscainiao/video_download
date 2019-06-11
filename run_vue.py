# -*- coding:utf-8 -*-
import os
import time

from download.vue_video_download import download_file
from threading import Thread
from common import functions, global_data
from common.log import log

redis_key = 'vue_video_tasks'
site_name = 'vue'


def DLD_FILE(task_list):
    p_list = list()
    for data in task_list:
        p = Thread(target=download_file, args=(data['video_id'], data['url'], site_name))
        p_list.append(p)
    for p in p_list:
        p.start()
    for p in p_list:
        p.join()


def print_status():
    log(global_data.log_path, 'info', end_time, '*' * 100)
    log(global_data.log_path, 'info', end_time, '本次下载开始时间: %s' % start_time)
    log(global_data.log_path, 'info', end_time, '本次下载结束时间: %s' % end_time)
    log(global_data.log_path, 'info', end_time, '本次获取任务数量: %s' % len(global_data.data_id_list))
    log(global_data.log_path, 'info', end_time, '本次获取任务数量: %s' % len(global_data.data_id_list))
    log(global_data.log_path, 'info', end_time, '本次获取下载成功数量: %s' % len(global_data.data_id_success_list))
    log(global_data.log_path, 'info', end_time, '本次获取下载失败数量: %s' % len(global_data.data_id_fail_list))
    log(global_data.log_path, 'info', end_time, '总任务列表如下：')
    log(global_data.log_path, 'info', end_time, global_data.data_id_list)
    log(global_data.log_path, 'info', end_time, '下载失败任务列表如下：')
    log(global_data.log_path, 'info', end_time, global_data.data_id_fail_list)
    log(global_data.log_path, 'info', end_time, '下载成功任务列表如下：')
    log(global_data.log_path, 'info', end_time, global_data.data_id_success_list)


def run(t_num=5):
    while True:
        task_list = functions.load_task(t_num, redis_key)
        if task_list:
            for task in task_list:
                task_id = task['video_id']
                global_data.data_id_list.append(task_id)
            DLD_FILE(task_list)
        else:
            break


if __name__ == '__main__':
    start_time = functions.get_time_now()
    log_name = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    log_name = ''.join([site_name, log_name, '.txt'])
    global_data.log_path = os.path.join(os.getcwd(), 'logs', log_name)
    log(global_data.log_path, 'info', start_time, '开始下载任务')
    run(t_num=5)
    end_time = functions.get_time_now()
    print_status()


