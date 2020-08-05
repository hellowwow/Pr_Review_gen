
def word_cnt(sentence):  #统计字数
    sentence = sentence.strip()
    word_list = sentence.split('，')
    cnt = 0
    for word in word_list:
        word_temp = word.strip()
        if len(word_temp) > 0:
            cnt += 1
    return cnt

def char_cnt(sentence):  #统计词数
    sentence = sentence.strip()
    cnt = 0
    for char in sentence:
        if char.isalpha() or char.isdigit():
            cnt += 1
    return cnt
print(char_cnt('你好 #,, ！aaaa123'))

if __name__ == '__main__':
    path = 'G:\\毛\\文字稿\\文字稿\\'  # 文件夹路径
    read_file_name = '98-114文字稿.txt'
    save_file_name = '98-114文字稿_result.txt'
    with open(path + save_file_name, 'w') as f:  #
        print("")
    with open(path + read_file_name, 'r', encoding='utf-8') as f:
        data = f.readlines()
    write = open(path + save_file_name, 'a')

    task_name1 = ['任务1-1','任务1-2','任务1-3','任务2-1','任务2-2','任务2-3']  # 需要统计词数
    task_name2 = ['任务3 朗读','任务4-1','任务4-2','任务5-1','任务5-2','反刍','3个未来事件']  # 需要统计字数
    # for line in data:
    #     print(line)
    #去空行
    sentence_list = []
    for i in range(len(data)):
        line_now = data[i].strip()
        if line_now != '':
            sentence_list.append(line_now)
    # for line in sentence_list:
    #     print(line)

    for i in range(len(sentence_list)):
        sentence = sentence_list[i]
        if sentence == task_name1[0]:
            print(sentence_list[i - 1], file=write)

        for task in task_name1:
            if sentence == task:
                cnt = 0
                for j in range(i + 1, len(sentence_list)):
                    if sentence_list[j] in task_name1 + task_name2:
                        break
                    cnt += word_cnt(sentence_list[j])
                print(task + '  词数：' + str(cnt), file=write)
                for j in range(i + 1, len(sentence_list)):
                    if sentence_list[j] in task_name1 + task_name2:
                        break
                    print(sentence_list[j], file=write)

        for task in task_name2:
            if sentence == task:
                cnt = 0
                for j in range(i + 1, len(sentence_list)):
                    if sentence_list[j] in task_name1 + task_name2:
                        break
                    if j + 1 != len(sentence_list) and sentence_list[j + 1] in task_name1:
                        break
                    cnt += char_cnt(sentence_list[j])
                print(task + '  字数：' + str(cnt), file=write)
                for j in range(i + 1, len(sentence_list)):
                    if sentence_list[j] in task_name1 + task_name2:
                        break
                    if j + 1 != len(sentence_list) and sentence_list[j + 1] in task_name1:
                        break
                    print(sentence_list[j], file=write)

                if task == '3个未来事件':
                    print('', file=write)

    write.close()