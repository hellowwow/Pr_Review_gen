import json
import csv

repo_list = []
head = ['repo_name','owner','url','stars','commit_counts','commit_comment_counts','pull_counts','pull_comment_counts','pull_commit_counts','pull_commit_comment_counts','pull_commit_code_comment_counts']
# repo_list.append(head)
# with open('repo_java_stars_top_20_0512.csv') as f:
#     reader = csv.reader(f)
#     for row in reader:
#         #print(row)
#         url = row[2]
#         if url != 'url':
#             row.append(0)
#             row.append(0)
#             row.append(0)
#             repo_list.append(row)


repo_list = []
with open('repo_java_stars_top_24.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        #print(row)
        url = row[2]
        if url != 'url':
            row[8] = 0
        repo_list.append(row)

cnt = 0
cnt2 = 0
with open('F:\\pull_commit_code_comment_0525','r', encoding='utf-8') as read_file:
    for line in read_file:
        # print(line)
        list = json.loads(line.strip())
        if isinstance(list, dict):
            print(list)
            cnt2 += 1
            continue
        for review_map in list:
            cnt += 1
            pull_request = review_map['pull_request_url'].strip()
            owner = pull_request.split('/')[4]
            repo = pull_request.split('/')[5]
            # print(pull_request, owner, repo)
            flag = 1
            for i in range(0, len(repo_list)):
                if owner == repo_list[i][1] and repo == repo_list[i][0]:
                    flag = 0
                    repo_list[i][8] += 1
                    break
            if flag == 1:
                print(pull_request, owner, repo)
                cnt2 += 1
print(cnt, cnt2)

with open('repo_java_stars_top_24.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    for row in repo_list:
        #print(row)
        writer.writerow(row)