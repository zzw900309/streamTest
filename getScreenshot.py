import os
from moviepy.editor import VideoFileClip
from PIL import Image

def extract_frames(video_path, output_path_folder, output_prefix, fps):
    clip = VideoFileClip(video_path)
    clip_length = clip.duration
    print(clip_length)
    for i in range(int(clip_length)//fps):
        clip.save_frame(os.path.join(output_path_folder,f"{output_prefix}_{(i+1)*fps}.png"), (i+1)*fps)

downloads_folder = os.path.join(os.path.expanduser('~'), 'Downloads/115download')
video_path = os.path.join(downloads_folder, f"snis-576-2.mp4")
output_path_folder = downloads_folder

# video_path = 'your_video.mp4'  # 替换为你的视频文件路径

output_prefix = 'screenshot'  # 输出文件的前缀
fps = 3
extract_frames(video_path, output_path_folder, output_prefix, fps)