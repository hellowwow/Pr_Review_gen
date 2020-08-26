import pickle
from prepare import extract
from prepare import filter
from prepare import tokenize_local

is_extract = 0
is_filter = 0
is_tokenize = 1
is_filter_length = 1 # 过滤长度使用令牌化后的长度统计
comment_length_min = 1
comment_length_max = 100
code_length_min = 1
code_length_max = 500

def check_length(comment, code_diff):
    comment_len = len(comment)
    code_len = len(code_diff)
    if comment_length_min <= comment_len <= comment_length_max and code_length_min <= code_len <= code_length_max:
        return True
    return False
def check_is_empty(code_diff):
    return False

def prepare():
    repo_file='../repo_java_stars_top_24.csv'
    pull_file='E:\\pr_review\\crawl_json\\pulls_0714'
    commit_file='E:\\pr_review\\crawl_json\\pull_commit_0715'
    commit_comment_file='E:\\pr_review\\crawl_json\\pull_commit_code_comment_0708',
    extract_result_file='E:\\pr_review\\data\\code_comment_0724'
    filter_result_file='E:\\pr_review\\data\\code_comment_flite_0724'
    core_data_file='E:\\pr_review\\data\\core_data_0728'
    if is_extract:
        extract.extract(repo_file, pull_file, commit_file, commit_comment_file, extract_result_file)
    if is_filter:
        filter.filter(extract_result_file, filter_result_file, filter_result_file + '.csv')
    if is_tokenize:
        core_data_list = []
        with open(filter_result_file, 'rb') as read_file:
            print("data loading..")
            data_list = pickle.load(read_file)
            print("loading complete")
            for data_map in data_list:
                core_data = {}
                core_data['repo'] = data_map['owner'] + ':' + data_map['repo']
                core_data['code_diff'] = data_map['code_diff']
                core_data['comment'] = data_map['comment']
                core_data['code_diff_token'] = tokenize_local.english_token(core_data['code_diff'])
                core_data['comment_token'] = tokenize_local.english_token(core_data['comment'])
                if is_filter_length and (check_length(core_data['comment_token'], core_data['code_diff_token']) == False or check_is_empty(core_data['code_diff_token']) == True):
                    continue
                core_data_list.append(core_data)
        print("源数据数：", len(data_list))
        print("现数据数：", len(core_data_list))
        with open(core_data_file, 'wb') as write_file:
            pickle.dump(core_data_list, write_file)

prepare()