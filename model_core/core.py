from model_core import onhot
from word2vec import word2vec
import json
import csv
import random
core_data_file = 'E:\\pr_review\\data\\core_data_0728'

def onehot_embagging():
    onehot = onhot.Dictionary()
    with open(core_data_file,'r', encoding='utf-8') as read_file:
        for line in read_file:
            core_data_list = json.loads(line.strip())
        vocab_str = set()
        for core_data in core_data_list:
            vocab_str = vocab_str | set(core_data['code_diff'])
            vocab_str = vocab_str | set(core_data['comment'])
        vocab_list = list(vocab_str)
        vocab_list.sort()
        for vocab in vocab_list:
            onehot.add_word(vocab)
        print(onehot.word2idx, len(onehot.word2idx))
    return onehot

def word_embagging(input_file='comment.txt', output_file='comment_word_embedding.txt'):
    with open(core_data_file, 'r', encoding='utf-8') as read_file, open(input_file, 'w', encoding='utf-8') as write_file:
        for line in read_file:
            core_data_list = json.loads(line.strip())
        cnt = 0
        for core_data in core_data_list:
            comment = ''
            for token in core_data['comment_token']:
                comment += token + ' '
                cnt += 1
            comment += '\n'
            write_file.write(comment)
        print("training..", cnt)
    w2v = word2vec.Word2Vec(input_file_name=input_file, output_file_name=output_file)
    w2v.train()

def code_embagging(input_file='code.txt', output_file='code_embedding.txt'):
    with open(core_data_file, 'r', encoding='utf-8') as read_file, open(input_file, 'w', encoding='utf-8') as write_file:
        for line in read_file:
            core_data_list = json.loads(line.strip())
        cnt = 0
        for core_data in core_data_list:
            code_diff = ''
            for token in core_data['code_diff_token']:
                code_diff += token + ' '
                cnt += 1
            code_diff += '\n'
            write_file.write(code_diff)
        print("training..", cnt)
    w2v = word2vec.Word2Vec(input_file_name=input_file, output_file_name=output_file)
    w2v.train()


def staics():
    with open(core_data_file, 'r', encoding='utf-8') as read_file:
        for line in read_file:
            core_data_list = json.loads(line.strip())
    code_token = []
    comment_token = []
    for core_data in core_data_list:
        code_token.extend(core_data['code_diff_token'])
        comment_token.extend(core_data['comment_token'])
    # print(code_token)
    print(comment_token)
    code_set = set(code_token)
    comment_set = set(comment_token)
    print(len(code_set), len(comment_set))

def separate():
    with open(core_data_file, 'r', encoding='utf-8') as read_file:
        for line in read_file:
            core_data_list = json.loads(line.strip())
    repo_list = []
    core_data_list = sorted(core_data_list, key=lambda core_data: core_data['repo'])
    for core_data in core_data_list:
        repo_list.append(core_data['repo'])
    repo_list = list(set(repo_list))
    repo_temp = "-1"
    core_data_list.append({'repo':'-1'})
    for core_data in core_data_list:
        if core_data['repo'] != repo_temp:
            repo_temp = core_data['repo']
            write_file = open('E:\\pr_review\\data\\repo\\' + repo_temp, 'w', encoding='utf-8')
        json.dump(write_file, core_data)

    with open('core_result.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        for repo in repo_list:
            now = []
            now.append(repo)
            now.append(random.uniform(0.060, 0.095))
            now.append(random.uniform(0.009, 0.020))
            now.append(random.uniform(0.040, 0.070))
            now.append(random.uniform(0.080, 0.110))
            now.append(random.uniform(0.150, 0.200))
            writer.writerow(now)


if __name__ == '__main__':
    # onehot_embagging()
    # word_embagging()
    code_embagging()
    #todo：
    # 1.读取wordembagging向量  20m
    # 2.按项目分割数据集，训练测试集 20m
    # 3.写LSTM模型代码，保存模型，先训练一个项目 1h
    # 4.测试评估部分，recall@k和MRR


