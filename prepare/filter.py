import pickle
import csv

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
def filter(code_comment_file='E:\\pr_review\\data\\commit_code_comment_0724',
           result_file='E:\\pr_review\\data\\commit_code_comment_flite_0724',
           result_csv_file='E:\\pr_review\\data\\code_comment_flite_0724.csv'):
    with open(code_comment_file,'rb') as read_file:
        data_list = pickle.load(read_file)
        for data_map in data_list:
            # print(data_map)
            if check_language(data_map['code_diff']) == False or check_language(data_map['comment']) == False:
                # print(data_map['code_diff'], data_map['comment'])
                # print("********************")
                continue
            if check_author(data_map) == False:
                continue
            # if check_is_contain(data_map['comment']) == False:
            #     continue

            data_list2.append(data_map)
    save_result(result_file, result_csv_file, data_list2)
    print(len(data_list), len(data_list2))

def save_result(result_file, result_csv_file, result_list):
    with open(result_file,'wb') as write_file:
        pickle.dump(result_list, write_file)

    head = ['repo','owner','pull_id','puller','pull_title','pull_body','commit_id','committer','commit_message','code_diff','comment','commenter','created_time','updated_time']
    with open(result_csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(head)
        for data_map in result_list:
            row = []
            for key in head:
                row.append(data_map[key])
            writer.writerow(row)
