import json
import csv
import pickle

# head = ['repo','owner','pull_id','puller','pull_title','pull_body','commit_id',
# 'committer','commit_message','code_diff','comment','commenter']

# 项目信息
def extract(repo_file='../repo_java_stars_top_24.csv', pull_file='E:\\pr_review\\crawl_json\\pulls_0714',
            commit_file='E:\\pr_review\\crawl_json\\pull_commit_0715', commit_comment_file='E:\\pr_review\\crawl_json\\pull_commit_code_comment_0708',
            result_file='E:\\pr_review\\data\\commit_code_comment_0724'):
    repo_list = []
    with open(repo_file) as f:
        reader = csv.reader(f)
        for row in reader:
            repo_list.append(row)


    print("提取pull信息ing...")
    pulls_map = {}
    with open(pull_file,'r', encoding='utf-8') as read_file:
        for line in read_file:
            # print(line)
            list = json.loads(line.strip())
            for pull_line in list:
                # print(pull_line)
                pull = {}
                pull['url'] = pull_line['url']
                pull['diff_url'] = pull_line['diff_url']
                pull['puller'] = pull_line['user']['login']
                pull['pull_title'] = pull_line['title']
                pull['pull_body'] = pull_line['body']
                pulls_map[pull['url']] = pull


    print("提取commit信息ing..")
    commit_map = {}
    with open(commit_file,'r', encoding='utf-8') as read_file:
        for line in read_file:
            list = json.loads(line.strip())
            for commit_line in list:
                # print(commit_line)
                commit = {}
                commit['url'] = commit_line['url']
                commit['commit_id'] = commit_line['sha']
                if commit_line['author'] == None or commit_line['author'] == {}:
                    commit['committer'] = commit_line['commit']['author']['name']
                else:
                    commit['committer'] = commit_line['author']['login']
                commit['commit_message'] = commit_line['commit']['message']
                commit_map[commit['commit_id']] = commit


    cnt1 = 0
    cnt2 = 0
    data_list = []
    with open(commit_comment_file,'r', encoding='utf-8') as read_file, open(result_file, 'wb') as write_file:
        for line in read_file:
            # print(line)
            list = json.loads(line.strip())
            for review_map in list:
                cnt1 += 1
                data = {}
                pull_url = review_map['pull_request_url'].strip()
                temp = pull_url.split('/')
                data['repo'] = temp[5]
                data['owner'] = temp[4]
                flag = 0
                for i in range(0, len(repo_list)):
                    if data['owner'] == repo_list[i][1] and data['repo'] == repo_list[i][0]:
                        flag = 1
                        break
                if flag == 0:
                    continue

                data['pull_id'] = temp[7]
                if pull_url in pulls_map:
                    pull = pulls_map[pull_url]
                    data['puller'] = pull['puller']
                    data['pull_title'] = pull['pull_title']
                    data['pull_body'] = pull['pull_body']
                else:
                    print(pull_url)
                    continue

                data['commit_id'] = review_map['commit_id']
                if data['commit_id'] in commit_map:
                    commit = commit_map[review_map['commit_id']]
                    data['committer'] = commit['committer']
                    data['commit_message'] = commit['commit_message']
                else:
                    print(data['commit_id'])
                    continue
                data['code_diff'] = review_map['diff_hunk']

                data['comment'] = review_map['body']
                if review_map['user'] == None:
                    data['commenter'] = None
                else:
                    data['commenter'] = review_map['user']['login']
                data['created_time'] = review_map['created_at']
                data['updated_time'] = review_map['updated_at']

                # print(data)
                cnt2 += 1
                data_list.append(data)
                # json.dump(data, write_file)
        pickle.dump(data_list, write_file)

    print(cnt1, cnt2)

