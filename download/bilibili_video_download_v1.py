# -*- coding:utf-8 -*-

'''
项目: B站视频下载

版本1: 加密API版,不需要加入cookie,直接即可下载1080p视频

20190422 - 增加多P视频单独下载其中一集的功能
'''
import imageio

from common.upload_video_qiniu import upload_video
from trans_video import transcode_video

imageio.plugins.ffmpeg.download()
import urllib.request
import requests, time, hashlib
from moviepy.editor import *
import os, sys
from common import global_data
from common.functions import update_is_download, rm_video

base_dir = 'D:\Blibli_video'
start_time = time.time()


# 访问API地址
def get_play_list(start_url, cid, quality):
    entropy = 'rbMCKn@KuamXWlPMoJGsKcbiJKUfkPF_8dABscJntvqhRSETg'
    appkey, sec = ''.join([chr(ord(i) + 2) for i in entropy[::-1]]).split(':')
    params = 'appkey=%s&cid=%s&otype=json&qn=%s&quality=%s&type=' % (appkey, cid, quality, quality)
    chksum = hashlib.md5(bytes(params + sec, 'utf8')).hexdigest()
    url_api = 'https://interface.bilibili.com/v2/playurl?%s&sign=%s' % (params, chksum)
    headers = {
        'Referer': start_url,  # 注意加上referer
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
    }
    # print(url_api)
    html = requests.get(url_api, headers=headers).json()
    # print(json.dumps(html))
    video_list = [html['durl'][0]['url']]
    # print(video_list)
    return video_list


# 下载视频
'''
 urllib.urlretrieve 的回调函数：
def callbackfunc(blocknum, blocksize, totalsize):
    @blocknum:  已经下载的数据块
    @blocksize: 数据块的大小
    @totalsize: 远程文件的大小
'''


def Schedule_cmd(blocknum, blocksize, totalsize):
    speed = (blocknum * blocksize) / (time.time() - start_time)
    # speed_str = " Speed: %.2f" % speed
    speed_str = " Speed: %s" % format_size(speed)
    recv_size = blocknum * blocksize

    # 设置下载进度条
    f = sys.stdout
    pervent = recv_size / totalsize
    percent_str = "%.2f%%" % (pervent * 100)
    n = round(pervent * 50)
    s = ('#' * n).ljust(50, '-')
    f.write(percent_str.ljust(8, ' ') + '[' + s + ']' + speed_str)
    f.flush()
    # time.sleep(0.1)
    f.write('\r')


def Schedule(blocknum, blocksize, totalsize):
    speed = (blocknum * blocksize) / (time.time() - start_time)
    # speed_str = " Speed: %.2f" % speed
    speed_str = " Speed: %s" % format_size(speed)
    recv_size = blocknum * blocksize

    # 设置下载进度条
    f = sys.stdout
    pervent = recv_size / totalsize
    percent_str = "%.2f%%" % (pervent * 100)
    n = round(pervent * 50)
    s = ('#' * n).ljust(50, '-')
    print(percent_str.ljust(6, ' ') + '-' + speed_str)
    f.flush()
    time.sleep(2)
    # print('\r')


# 字节bytes转化K\M\G
def format_size(bytes):
    try:
        bytes = float(bytes)
        kb = bytes / 1024
    except:
        print("传入的字节格式不对")
        return "Error"
    if kb >= 1024:
        M = kb / 1024
        if M >= 1024:
            G = M / 1024
            return "%.3fG" % (G)
        else:
            return "%.3fM" % (M)
    else:
        return "%.3fK" % (kb)


#  下载视频
def down_video(video_list, title, start_url):
    num = 1
    # print('[正在下载视频]：{}:'.format(title))
    currentVideoPath = os.path.join(base_dir, title)  # 当前目录作为下载目录
    for i in video_list:
        opener = urllib.request.build_opener()
        # 请求头
        opener.addheaders = [
            # ('Host', 'upos-hz-mirrorks3.acgvideo.com'),  #注意修改host,不用也行
            ('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:56.0) Gecko/20100101 Firefox/56.0'),
            ('Accept', '*/*'),
            ('Accept-Language', 'en-US,en;q=0.5'),
            ('Accept-Encoding', 'gzip, deflate, br'),
            ('Range', 'bytes=0-'),  # Range 的值要为 bytes=0- 才能下载完整视频
            ('Referer', start_url),  # 注意修改referer,必须要加的!
            ('Origin', 'https://www.bilibili.com'),
            ('Connection', 'keep-alive'),
        ]

        urllib.request.install_opener(opener)
        # 创建文件夹存放下载的视频
        if not os.path.exists(currentVideoPath):
            os.makedirs(currentVideoPath)
        # 开始下载
        if len(video_list) > 1:
            urllib.request.urlretrieve(url=i, filename=os.path.join(currentVideoPath, r'{}-{}.flv'.format(title, num))
                                       )
        else:
            urllib.request.urlretrieve(url=i, filename=os.path.join(currentVideoPath, r'{}.flv'.format(title))
                                       )


# 合并视频
def combine_video(video_list, title):
    currentVideoPath = os.path.join(base_dir, title)  # 当前目录作为下载目录
    if len(video_list) >= 2:
        # 视频大于一段才要合并
        print('[下载完成,正在合并视频...]:' + title)
        # 定义一个数组
        L = []
        # 访问 video 文件夹 (假设视频都放在这里面)
        root_dir = currentVideoPath
        # 遍历所有文件
        for file in sorted(os.listdir(root_dir), key=lambda x: int(x[x.rindex("-") + 1:x.rindex(".")])):
            # 如果后缀名为 .mp4/.flv
            if os.path.splitext(file)[1] == '.flv':
                # 拼接成完整路径
                filePath = os.path.join(root_dir, file)
                # 载入视频
                video = VideoFileClip(filePath)
                # 添加到数组
                L.append(video)
        # 拼接视频
        final_clip = concatenate_videoclips(L)
        # 生成目标视频文件
        final_clip.to_videofile(os.path.join(root_dir, r'{}.flv'.format(title)), fps=24, remove_temp=False)
        print('[视频合并完成]' + title)

    else:
        # 视频只有一段则直接打印下载完成
        print('[视频下载完成]：' + title)


def download_file(data_id, cid):
    data_id, cid = str(data_id), str(cid)
    quality = '64'
    start_url = 'https://api.bilibili.com/x/web-interface/view?aid=' + data_id
    try:
        video_list = get_play_list(start_url, cid, quality)
    except Exception as e:
        print('----------------%s get video_list fail: %s----------------' % (data_id, str(e)))
        global_data.data_id_fail_list.append(data_id)
        return None
    try:
        down_video(video_list, data_id, start_url)            # 下载
    except Exception as e:
        print('-----------------%s 下载失败, %s-----------------' % (data_id, str(e)))
        global_data.data_id_fail_list.append(data_id)
        rm_video(data_id)
        return None
    combine_video(video_list, data_id)
    transcode_video(data_id)     # 转码
    try:
        upload_video(data_id)    # 上传
        print('[视频上传完成]：%s' % data_id)
    except Exception as e:
        print('======================== %s 上传失败： %s ==========================' % (data_id, str(e)))
        rm_video(data_id)
        return
    try:
        update_is_download(data_id, 'data_blibli_download')
        global_data.data_id_success_list.append(data_id)
    except Exception as e:
        print('======================== %s 更新状态失败： %s ==========================' % (data_id, str(e)))
    rm_video(data_id)              # 删除


if __name__ == '__main__':
    download_file(40505453, 71137356)
