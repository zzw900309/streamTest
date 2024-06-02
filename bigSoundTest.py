'''
- 将视频分割为时长为X秒的小段落，并根据平均音量排序；
- 将top音量的小段视频进行拼接，组成一个完整视频；
'''

import os
import math
from pydub import AudioSegment
from moviepy.editor import VideoFileClip, concatenate_videoclips

def extract_clips(video_path, clip_duration, interval):
    # 加载视频
    clip = VideoFileClip(video_path)
    clip_length = clip.duration
    clipsTemp = []
    start_time = 0
    iCount = 0

    # 确保片段时长是合理的
    if clip_duration > 0:
        while start_time < clip_length:
            clipsTemp.append([iCount])
            clipsTemp[iCount].append(start_time)
            # 截取片段
            if start_time <= clip_length - clip_duration:
                clip_to_save = clip.subclip(start_time, start_time + clip_duration)
            else:
                clip_to_save = clip.subclip(start_time, clip_length)  # 处理最后一个片段
            clipsTemp[iCount].append(clip_to_save)

            # 生成临时音频文件
            audioTemp = clip_to_save.audio
            audio_filename = f"temp_audio_{iCount}.mp3"
            audioTemp.write_audiofile(audio_filename)
            # 加载音频文件
            audio = AudioSegment.from_file(audio_filename, format="mp3")
            # 获取音频样本的数组
            samples = audio.get_array_of_samples()
            # 计算总音量（累加样本的平方值）
            total_volume = sum(sample ** 2 for sample in samples)
            # 计算平均音量（取平方根以更接近人耳对音量的感知）
            average_volume_rms = round(math.sqrt(total_volume / len(samples)), 2)
            # 存储平均音量
            clipsTemp[iCount].append(average_volume_rms)
            # 清理临时音频文件（可选）
            os.remove(audio_filename)

            # 更新起始时间，加上间隔
            iCount += 1
            start_time += interval

    print(f"一共{iCount}个片段，分割处理完成！")

    return clipsTemp

def findVideoFunc(folder_path):
    fileNameList = []
    # 遍历目录
    for filename in os.listdir(folder_path):
        if filename.endswith('.mp4'):
            fileNameList.append(filename)
            print(filename)
    return fileNameList

rankList = []
# 设置视频目录文件夹路径
downloads_folder = os.path.join(os.path.expanduser('~'), 'Downloads/115download')
# 遍历文件夹，返回视频
video_path_list = findVideoFunc(downloads_folder)
# 截取片段的时长（秒）
clip_duration_in_seconds = 6
# 截取片段的间隔（秒）
interval_in_seconds = clip_duration_in_seconds

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
    # 提取片段，计算平均音量
    clips = extract_clips(video_path, clip_duration_in_seconds, interval_in_seconds)

    # 使用音量平均值来排序
    clips.sort(key=lambda x: x[3], reverse= True)

    # 获取排名前20的片段
    rankList.clear()
    for i in range(20):
        rankList.append(clips[i])
    rankList.sort(key=lambda x: x[0], reverse= False)

    # 拼接选出的片段
    i2 = 0
    for clipOne in rankList:
        if i2 == 0:
            clipFinal = clipOne[2]
        if i2 > 0:
            clipFinal = concatenate_videoclips([clipFinal,clipOne[2]])
        i2 += 1

    # 输出视频
    clip_name = f"{output_prefix}.mp4"
    clipFinal.write_videofile(clip_name, audio_codec='aac')






'''

rankTempList = []
rankLeaveList = []
# 重建排序队列
for j in range(len(clips)):
    rankTempList.append([j])
    rankTempList[j].append(1)

for i in range(len(clips)):
    try:
        indexNow = rankTempList.index([clips[i][0],1])
        rankTempList[indexNow][1] = 2
        rankLeaveList.append(clips[i][0])
        for i2 in range(3):
            try:
                if rankTempList[indexNow+i2+1][1] < 2:
                    rankTempList[indexNow+i2+1][1] = 0
            except:
                pass
            try:
                if rankTempList[indexNow-i2-1][1] < 2:
                    rankTempList[indexNow-i2-1][1] = 0
            except:
                pass
    except:
        pass

print(rankLeaveList)

if len(rankLeaveList) >= 5:
    for k in range(20):
        for k2 in clips:
            if rankLeaveList[k] == k2[0]:
                clip_name = f"{k+1}_{rankLeaveList[k]}_clip_{k2[1]}.mp4"
                k2[2].write_videofile(clip_name, audio_codec='aac')'''



'''for k, clip in clips:
    clip_name = f"{clip[k]}_clip_{clip[1]}.mp4"
    clip[2].write_videofile(clip_name, audio_codec='aac')'''




'''plt.plot(x, soundResult)
plt.show()'''

