from pydub import AudioSegment
from pydub.silence import detect_silence
import os
from pandas import DataFrame

def remove_silence(sound_path, sound_name, save_path):

    # f = wave.open(path + sound_path,'rb')
    # print(f.getparams())
    print('cutting ' + sound_name + '....')
    sound = AudioSegment.from_wav(sound_path + sound_name)
    sound_length = len(sound)
    silence_length = 0
    #得到沉默时间片段
    start_end = detect_silence(sound,10,-40,1)
    # print(len(start_end_temp), start_end_temp)

    #合并距离很近的片段，去除空格影响
    start_end_temp = []
    if len(start_end) == 0:
        sound.export(save_path + sound_name, format='wav')
    else:
        start_end_temp.append(start_end[0])
        for i in range(1, len(start_end)):
            if start_end[i][0] - start_end[i-1][1] < 50:
                start_end_temp[len(start_end_temp) - 1][1] = start_end[i][1]
            else:
                start_end_temp.append(start_end[i])
        # print(len(start_end_temp), start_end_temp)

        start_end = []
        for line in start_end_temp:
            if line[1] - line[0] >= 300:
                start_end.append(line)


        # print(time_change(1254))
        # print(time_change(3993))
        # [00:01.254]
        # [00:03.993]
        time_list = []

        for line in start_end:
            silence_length += line[1] - line[0]
            start_time = time_change(line[0])
            end_time = time_change(line[1])
            time_list.append([start_time, end_time])

        # 把沉默时间剪掉
        # ten_seconds = 10 * 1000
        # first_10_seconds = sound[:ten_seconds]
        # first_10_seconds.export(path + 'first_10.wav', format='wav')

        # print(no_silence_sounds.sample_width)
        if len(start_end) == 0:
            sound.export(save_path + sound_name, format='wav')
        else:
            no_silence_sounds = sound[0: start_end[0][0]]
            for i in range(1, len(start_end)):
                no_silence_sounds = no_silence_sounds + sound[start_end[i-1][1] : start_end[i][0]]
            no_silence_sounds = no_silence_sounds + sound[start_end[len(start_end) - 1][1] : -1]
            no_silence_sounds = no_silence_sounds.set_sample_width(3)
            no_silence_sounds.export(save_path + sound_name, format='wav')

    result_list = []
    result_list.append(len(start_end))                              #沉默次数
    result_list.append(time_change(sound_length))                   #回答时长
    result_list.append(time_change(silence_length))                 #沉默时长
    result_list.append(time_change(sound_length - silence_length))  #发声时长
    print(result_list)
    return result_list

#将毫秒级时间转化为时分秒
def time_change(time):
    h, hs = divmod(float(time), 3600000)
    m, ms = divmod(float(hs), 60000)
    s, ms = divmod(float(ms), 1000)
    ts = "%02d:%02d:%02d.%03d" % (h, m, s, ms)
    return str(ts)

def get_files(dir): #得到路径下的所有子文件
    files_ = []
    list_ = os.listdir(dir)
    for i in range(0, len(list_)):
        path = os.path.join(dir, list_[i])
        if os.path.isfile(path):
            files_.append(list_[i])
    return files_

def get_dir(dir): #得到路径下的所有子文件夹
    files_ = []
    list_ = os.listdir(dir)
    for i in range(0, len(list_)):
        path = os.path.join(dir, list_[i])
        if os.path.isdir(path):
            files_.append(list_[i])
    return files_

def mkdir(path):  #创建文件夹
    path = path.strip()
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        return True
    return False

#生成csv文件，打开日期格式有问题
# if __name__ == '__main__':
#     path = 'G:\\毛\\音频文件\\'    #文件夹路径
#     silence_sounds_path = 'G:\\毛\\无沉默音频\\'
#     # sound_path = '093-反刍-剪之前.wav'
#
#     file_head = ['3个未来事件','任务3-朗读','任务4-看图1','任务4-看图2','任务5-想象工作','任务5-成就感','反刍']
#     length_head = ['沉默次数','回答时长','沉默时长','发声时长']
#     head = ['编号']
#     for file in file_head:
#         for length in length_head:
#             head.append(file + '_' + length)
#
#     with open(silence_sounds_path +'音频统计.csv', 'w', newline='',encoding='utf-8') as f:
#         writer = csv.writer(f)
#         writer.writerow(head)
#         Participant_ID_list = get_dir(path)
#         for Participant_ID in Participant_ID_list:
#             result_list = [Participant_ID]
#             mkdir(silence_sounds_path + Participant_ID)
#             sound_list = get_files(path + Participant_ID + '\\')
#             print(sound_list)
#             for sound_name in sound_list:
#                 length_list = remove_silence(path + Participant_ID + '\\', sound_name, silence_sounds_path + Participant_ID + '\\')
#                 for length in length_list:
#                     result_list.append(length)
#             print(result_list)
#             writer.writerow(result_list)




if __name__ == '__main__':
    path = 'G:\\毛\\音频剪辑\\'    #文件夹路径
    silence_sounds_path = 'G:\\毛\\无沉默音频\\'
    # sound_path = '093-反刍-剪之前.wav'

    file_head = ['3个未来事件','任务3-朗读','任务4-看图1','任务4-看图2','任务5-想象工作','任务5-成就感','反刍']
    length_head = ['沉默次数','回答时长','沉默时长','发声时长']
    head = ['编号']  #表头
    for file in file_head:
        for length in length_head:
            head.append(file + '_' + length)
    sound_df = DataFrame([], columns=head)

    Participant_ID_list = get_dir(path)
    # print(Participant_ID_list)
    for Participant_ID in Participant_ID_list:
        result_list = [Participant_ID]  #一个被试的结果
        mkdir(silence_sounds_path + Participant_ID)
        sound_list = get_files(path + Participant_ID + '\\')
        print(sound_list)
        for sound_name in sound_list:
            length_list = remove_silence(path + Participant_ID + '\\', sound_name, silence_sounds_path + Participant_ID + '\\')
            for length in length_list:
                result_list.append(length)

        sound_df = sound_df.append(DataFrame([result_list], columns=head), ignore_index=True)

    print(sound_df.head())
    sound_df.to_excel(silence_sounds_path + '音频统计.xlsx')

