import os

def transcode_video(video_id):
    ffmpeg = "ffmpeg.exe"
    video_id = str(video_id)
    base_dir = 'D:\Blibli_video'
    in_path = os.path.join(base_dir, video_id, video_id + '.flv')
    out_path = os.path.join(base_dir, video_id, video_id + '.mp4')
    # cmd = ffmpeg + " -i " + in_path + ' -b:v 2400k -bufsize 2400k ' + ' -vf scale=1280:720 '\
    #      + out_path + ' > D:trans.txt 2>&1'
    cmd = ffmpeg + " -i " + in_path + ' -c copy ' + out_path + ' > D:trans.txt 2>&1'
    os.system(cmd)