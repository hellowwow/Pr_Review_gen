import os
import csv



def get_all_files(dir):
    files_ = []
    list_ = os.listdir(dir)
    for i in range(0, len(list_)):
        path = os.path.join(dir, list_[i])
        if os.path.isdir(path):
            files_.extend(get_all_files(path))
        if os.path.isfile(path):
            files_.append(list_[i])
    return files_

def get_files(dir):
    files_ = []
    list_ = os.listdir(dir)
    for i in range(0, len(list_)):
        path = os.path.join(dir, list_[i])
        if os.path.isdir(path):
            files_.append(list_[i])
    return files_

dir = 'G:\\研\\研一课程\\软件体系结构\\作业\\第七次作业\\FreeCAD-master\\FreeCAD-master\\src\\mod'

file_list = get_files(dir)
print(file_list)

with open('language_counts.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['模块名','.cpp文件数量','.py文件数量'])
    for moudle_name in file_list:
        files = get_all_files(dir + '\\' + moudle_name)
        count_list = [moudle_name, 0, 0]
        for file in files:
            houzui = file.split('.')[-1]
            if houzui == 'py':
                count_list[2] += 1
            if houzui == 'cpp':
                count_list[1] += 1
        writer.writerow(count_list)
