import os
from moviepy.editor import VideoFileClip
import subprocess

# def extract_frames(video_path, output_path_folder, output_prefix, fps):

def split_video(video_path, output_path_folder, output_prefix, fps):

    clip = VideoFileClip(video_path)
    clip_length = clip.duration
    print(clip_length, int(clip_length)//fps)
    for i in range(int(clip_length)//fps):
        imgpath = os.path.join(output_path_folder, f"{output_prefix}_{i*fps}.png")
        clip.save_frame(imgpath, i*fps)

    '''for i in range(int(clip_length) // fps):
        command = [
            'ffmpeg',
            '-ss', f'{i*fps}',
            '-t', f'{fps}',
            '-accurate_seek',
            '-i', video_path,
            '-c', 'copy',
            '-avoid_negative_ts', '1',
            os.path.join(output_path_folder,f"{output_prefix}_{i*fps}.mp4")
        ]
        """
        分割视频函数
        :param input_video: 输入视频文件名
        :param output_prefix: 输出视频文件名前缀
        :param start_time: 分割开始时间（秒）
        :param duration: 分割持续时间（秒）
        """
        subprocess.run(command, check=True)'''

def findVideoFunc(folder_path):
    fileNameList = []
    # 遍历目录
    for filename in os.listdir(folder_path):
        if filename.endswith('.mp4'):
            fileNameList.append(filename)
            print(filename)
    return fileNameList

# 原视频文件夹
downloads_folder = os.path.join(os.path.expanduser('~'), 'Downloads/115download')
# 每段长度（秒）
fps = 3
# 遍历文件夹，返回视频
video_path_list = findVideoFunc(downloads_folder)

for video_path_name in video_path_list:
    # 创建输出文件夹
    video_name = video_path_name.split(".")[0]
    folder_name = video_name
    path = downloads_folder + "/" + folder_name
    os.makedirs(path, exist_ok=True)
    output_path_folder = path
    # 输出文件的前缀
    output_prefix = video_name
    # 输入文件
    video_path = os.path.join(downloads_folder, video_path_name)
    split_video(video_path, output_path_folder, output_prefix, fps)