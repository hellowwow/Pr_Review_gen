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
            row[7] = 0
        repo_list.append(row)

cnt = 0
cnt2 = 0
for index in range(1,3):
    with open('F:\\pull_commit_comment_0604_' + str(index), 'r', encoding='utf-8') as read_file:
        for line in read_file:
            # print(line)
            list = json.loads(line.strip())
            # if isinstance(list, dict):
            #     print(list)
            #     cnt2 += 1
            #     continue
            for review_map in list:
                comment_url = review_map['url'].strip()
                owner = comment_url.split('/')[4]
                repo = comment_url.split('/')[5]
                print(comment_url, owner, repo)
                for i in range(0, len(repo_list)):
                    if owner == repo_list[i][1] and repo == repo_list[i][0]:
                        repo_list[i][7] += 1
                        break
print(cnt, cnt2)

with open('repo_java_stars_top_24.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    for row in repo_list:
        #print(row)
        writer.writerow(row)