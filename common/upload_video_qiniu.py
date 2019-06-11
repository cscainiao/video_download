# -*- coding: utf-8 -*-
# flake8: noqa
import os
from qiniu import Auth, put_file, etag,urlsafe_base64_encode
import qiniu.config

def upload_video(video_id,site_name='t'):
    video_id = str(video_id)
    base_dir = 'D:\Blibli_video'
    file_path = os.path.join(base_dir, video_id, video_id + '.mp4')

    #需要填写你的 Access Key 和 Secret Key
    access_key = 'vECq3gaU9nYuFCg5-XPf8vG5ia0I55XHFhFN_bYO'
    secret_key = 'HLO0bvRW0rwSDHV5J3slQ4-zbtY_OTOjTAjZMrLu'

    #构建鉴权对象
    q = Auth(access_key, secret_key)

    #要上传的空间
    bucket_name = 'video'

    #上传后保存的文件名
    key = video_id + '-%s.mp4' % site_name
    # key='$(%s)-transcode.$(mp4)' % video_id

    fops = 'avthumb/mp4/ab/128k/ar/44100/acodec/libfaac/r/30/vb/900k/vcodec/libx264/s/640x480/autoscale/1/stripmeta/0'
    # pipeline = 'mebvideo'
    # #可以对转码后的文件进行使用saveas参数自定义命名，当然也可以不指定文件会默认命名并保存在当前空间
    saveas_key = urlsafe_base64_encode('video:%s' % key)
    fops = fops+'|saveas/'+saveas_key
    saveKey = "$(fprefix)-%s$(ext)" % site_name
    policy = {
      'persistentOps': fops,
      # 'persistentPipeline': pipeline,
      'saveKey': saveKey
     }
    #生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket=bucket_name, expires=3600, policy=policy)

    #要上传文件的本地路径
    localfile = file_path

    ret, info = put_file(token, None, localfile)
    if info.status_code == 614:
        return
    assert ret['key'] == key
