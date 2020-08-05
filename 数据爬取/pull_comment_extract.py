import json
import csv

repo_list = []
with open('repo_java_stars_top_24.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        #print(row)
        url = row[2]
        if url != 'url':
            row[5] = 0
        repo_list.append(row)

for index in range(1,4):
    with open('F:\\pull_comment_0528_' + str(index), 'r', encoding='utf-8') as read_file:
        for line in read_file:
            # print(line)
            list = json.loads(line.strip())
            # if isinstance(list, dict):
            #     print(list)
            #     cnt2 += 1
            #     continue
            for review_map in list:
                pull_request = review_map['url'].strip()
                owner = pull_request.split('/')[4]
                repo = pull_request.split('/')[5]
                print(pull_request, owner, repo)
                for i in range(0, len(repo_list)):
                    if owner == repo_list[i][1] and repo == repo_list[i][0]:
                        repo_list[i][5] += 1
                        break

with open('repo_java_stars_top_24.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    for row in repo_list:
        #print(row)
        writer.writerow(row)