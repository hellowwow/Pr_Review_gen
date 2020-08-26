#数据分析
import pickle
import csv
from prepare import tokenize_local

comment_max_len = 1000
code_max_len = 10000

# todo:如何更好的度量代码的长度，令牌方式    word2vec嵌入编码
def comment_length(review):
    return len(tokenize_local.english_token(review, 2, 0, 2, 2))
    # return len(review.split())

def code_length(code_diff):
    tokens = tokenize_local.code_token(code_diff)
    length = 0
    for token in tokens:
        if str(token[0]) != 'Token.Text' and str(token[0]) != 'Token.Punctuation':
            length += 1
    return length
#
# example_text = 'System.out.println("Hello " + "world");'
# print(code_length(example_text))

comment_lens = []
for i in range(comment_max_len + 2):
    comment_lens.append(0)

code_lens = []
for i in range(code_max_len + 2):
    code_lens.append(0)

data_len = 0
def comment_length_counts():
    max_comment_len = 0
    sum_comment_len = 0
    with open('E:\\pr_review\\data\\commit_code_comment_flite_0724','rb') as read_file:
        data_list = pickle.load(read_file)
        data_len = len(data_list)
        for data_map in data_list:
            comment_len = comment_length(data_map['comment'])
            if comment_len == 5:
                print(data_map['comment'])

            max_comment_len = max(max_comment_len, comment_len)
            sum_comment_len += comment_len
            if comment_len <= comment_max_len:
                comment_lens[comment_len] += 1
            else:
                comment_lens[comment_max_len + 1] += 1

    with open('comment_len_counts_have_stop_words.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        for i in range(comment_max_len + 2):
            writer.writerow([i, comment_lens[i]])
        writer.writerow([max_comment_len, sum_comment_len, sum_comment_len / data_len])
        print(max_comment_len, sum_comment_len, sum_comment_len / data_len)

def code_length_counts():
    max_code_len = 0
    sum_code_len = 0
    with open('E:\\pr_review\\data\\commit_code_comment_flite_0724','rb') as read_file:
        data_list = pickle.load(read_file)
        data_len = len(data_list)
        for data_map in data_list:
            # if code_length(data_map['code_diff']) == 2:
            #     print(data_map['code_diff'])
            #     print("")

            code_len = code_length(data_map['code_diff'])
            if code_len <= 10:
                print(data_map['code_diff'])
                print("")

            max_code_len = max(max_code_len, code_len)
            sum_code_len += code_len
            if code_len <= code_max_len:
                code_lens[code_len] += 1
            else:
                code_lens[code_max_len + 1] += 1
    with open('code_len_counts.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        for i in range(code_max_len + 2):
            writer.writerow([i, code_lens[i]])
        writer.writerow([max_code_len, sum_code_len, sum_code_len / data_len])
        print(max_code_len, sum_code_len, sum_code_len / data_len)

def comment_length_statisitcs():
    len_temp = 12
    comment_len_list = [[1, 2, 5, 10, 20, 50, 75, 100, 200, 500, 1000, 2000], [0,0,0,0,0,0,0,0,0,0,0,0,0]]
    with open('E:\\pr_review\\data\\commit_code_comment_flite_0724', 'rb') as read_file:
        data_list = pickle.load(read_file)
        data_len = len(data_list)
    with open('comment_len_counts.csv') as read_file:
        reader = csv.reader(read_file)
        index_now = 0
        for row in reader:
            length, count = int(row[0]), int(row[1])
            while length > comment_len_list[0][index_now]:
                print(length, comment_len_list[0][index_now])
                index_now += 1
            comment_len_list[1][index_now] += count
    with open('comment_statisitcs.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        sum = 0
        for i in range(len_temp):
            sum += comment_len_list[1][i]
            writer.writerow(['<=' + str(comment_len_list[0][i]), sum, '{:.2%}'.format(sum / data_len)])
            print('<=' + str(comment_len_list[0][i]), sum, '{:.2%}'.format(sum / data_len))


def code_length_statisitcs():
    len_temp = 16
    code_len_list = [[2,5,10,20,50,70,100,200,300,400,500,1000,2000,5000,10000, 20000], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
    with open('E:\\pr_review\\data\\commit_code_comment_flite_0724', 'rb') as read_file:
        data_list = pickle.load(read_file)
        data_len = len(data_list)
    with open('code_len_counts.csv') as read_file:
        reader = csv.reader(read_file)
        index_now = 0
        for row in reader:
            length, count = int(row[0]), int(row[1])
            while length > code_len_list[0][index_now]:
                print(length, code_len_list[0][index_now])
                index_now += 1
            code_len_list[1][index_now] += count
    with open('code_statisitcs.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        sum = 0
        for i in range(len_temp):
            sum += code_len_list[1][i]
            writer.writerow(['<=' + str(code_len_list[0][i]), sum, '{:.2%}'.format(sum / data_len)])
            print('<=' + str(code_len_list[0][i]), sum, '{:.2%}'.format(sum / data_len))


if __name__ == '__main__':
    comment_length_counts()