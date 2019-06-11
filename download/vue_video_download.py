import os

import requests, random, socket
import urllib.request

from common import global_data
from common.functions import update_is_download, rm_video, get_ip, get_ip_api
from common.upload_video_qiniu import upload_video


base_dir = 'D:\Blibli_video'

def down_video(data_id, url):
    currentVideoPath = os.path.join(base_dir, data_id)
    if not os.path.exists(currentVideoPath):
        os.makedirs(currentVideoPath)

    # if global_data.ip_ok:
    #     ip = global_data.ip_ok.pop()
    # else:
    #     ip = get_ip()
    # proxies = 'http://' + ip
    # proxy = urllib.request.ProxyHandler({'http': proxies})
    # opener = urllib.request.build_opener(proxy, urllib.request.HTTPHandler)
    opener = urllib.request.build_opener()
    opener.addheaders = [
        ('User-Agent', 'Dalvik/2.1.0 (Linux; U; Android 5.1.1; OPPO R11 Plus Build/LMY48Z)'),
        ('Connection', 'keep-alive'),
    ]

    urllib.request.install_opener(opener)
    socket.setdefaulttimeout(30)
    urllib.request.urlretrieve(url=url, filename=os.path.join(currentVideoPath, r'{}.mp4'.format(data_id)))
    # global_data.ip_ok.append(ip)


def download_file(data_id, url, site_name='t'):
    data_id = str(data_id)
    try:
        down_video(data_id, url)            # 下载
        print('[视频下载完成]：%s' % data_id)
    except Exception as e:
        print('-----------------%s 下载失败, %s-----------------' % (data_id, str(e)))
        global_data.data_id_fail_list.append(data_id)
        rm_video(data_id)  # 删除
        return None
    try:
        upload_video(data_id, site_name)    # 上传
        print('[视频上传完成]：%s' % data_id)
    except Exception as e:
        print('======================== %s 上传失败： %s ==========================' % (data_id, str(e)))
        return

    global_data.data_id_success_list.append(data_id)
    try:
        update_is_download(data_id, site_name)
    except Exception as e:
        print('======================== %s 更新状态失败： %s ==========================' % (data_id, str(e)))
    rm_video(data_id)              # 删除


if __name__ == '__main__':
    download_file(-7608423088668828439,'http://video.cdnvue.com/uploads/736160548418701590/video/bbt2IgJ','vue')