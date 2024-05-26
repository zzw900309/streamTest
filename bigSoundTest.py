import copy
import os
import math
from pydub import AudioSegment
from moviepy.editor import VideoFileClip, concatenate_videoclips

def extract_clips(video_path, clip_duration, interval):
    clip = VideoFileClip(video_path)
    clip_length = clip.duration
    clipsTemp = []
    start_time = 0
    iCount = 0

    # 确保间隔和片段时长是合理的
    # if interval <= clip_duration and clip_duration > 0:
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


rankList = []
rankTempList = []
rankLeaveList = []

# 视频文件夹路径 - Downloads
downloads_folder = os.path.join(os.path.expanduser('~'), 'Downloads/115download')
# 视频文件路径
video_path = os.path.join(downloads_folder, f"snis-576-2.mp4")

# 截取片段的时长（秒）
clip_duration_in_seconds = 6  # 2分钟
# 截取片段的间隔（秒）
interval_in_seconds = 6

# 提取片段，计算平均音量
clips = extract_clips(video_path, clip_duration_in_seconds, interval_in_seconds)

# 使用音量平均值来排序
clips.sort(key=lambda x: x[3], reverse= True)
print(clips)

'''
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

for i in range(20):
    rankList.append(clips[i])
rankList.sort(key=lambda x: x[0], reverse= False)

i2 = 0
for clipOne in rankList:
    if i2 == 0:
        clipFinal = clipOne[2]
    if i2 > 0:
        clipFinal = concatenate_videoclips([clipFinal,clipOne[2]])
    print(clipOne[0])
    i2 += 1

clip_name = f"finalClip.mp4"
clipFinal.write_videofile(clip_name, audio_codec='aac')

'''for k, clip in clips:
    clip_name = f"{clip[k]}_clip_{clip[1]}.mp4"
    clip[2].write_videofile(clip_name, audio_codec='aac')'''




'''plt.plot(x, soundResult)
plt.show()'''

