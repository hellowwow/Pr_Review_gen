import pickle
import csv

comment_length_max = 100
comment_length_min = 0
code_length_max = 5000
code_length_min = 0

def comment_length(str):
    return len(str.split())

def code_length(str):
    return len(str)

def check_length(comment, code_diff):
    comment_len = comment_length(comment)
    code_len = code_length(code_diff)
    if comment_length_min <= comment_len <= comment_length_max and code_length_min <= code_len <= code_length_max:
        return True
    return False
def check_is_empty(code_diff):
    return False

chara = '~`!@#$%^&*()-_+-=/*-+.\\|]}[{\'";:/?.>,< \t\n\r'
def check_language(str):
    for i in str:
        if not (i.encode('utf-8').isalpha() or i.isdigit() or i in chara):
            # print(i)
            return False
    return True

def check_author(data):
    if data['commenter'] == data['puller'] or data['commenter'] == data['committer']:
        return False
    return True

def check_is_contain(str):
    word_list = ['thank you','thanks','You’re right','It works','ok', 'Ack']
    for word in word_list:
        if word in str:
            return False
    return True
# print(check_language("ab12"))

data_list2 = []
with open('E:\\pr_review\\data\\commit_code_comment_0724','rb') as read_file:
    data_list = pickle.load(read_file)
    for data_map in data_list:
        # print(data_map)
        if check_language(data_map['code_diff']) == False or check_language(data_map['comment']) == False:
            # print(data_map['code_diff'], data_map['comment'])
            # print("********************")
            continue
        if check_author(data_map) == False:
            continue
        # if check_length(data_map['comment'], data_map['code_diff']) == False or check_is_empty(data_map['code_diff']) == True:
        #     continue
        # if check_is_contain(data_map['comment']) == False:
        #     continue

        data_list2.append(data_map)
    print(len(data_list), len(data_list2))

with open('E:\\pr_review\\data\\commit_code_comment_flite_0724','wb') as write_file:
    pickle.dump(data_list2, write_file)

head = ['repo','owner','pull_id','puller','pull_title','pull_body','commit_id','committer','commit_message','code_diff','comment','commenter','created_time','updated_time']
with open('E:\\pr_review\\data\\code_review_0724.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(head)
    for data_map in data_list2:
        row = []
        for key in head:
            row.append(data_map[key])
        writer.writerow(row)
