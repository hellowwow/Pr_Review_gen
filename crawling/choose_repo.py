import csv
# # 选前20个项目
# with open('repo_java_stars_top_24.csv') as f, open('repo_java_stars_top_20_0512.csv', 'w', newline='') as wri:
#     reader = csv.reader(f)
#     writer = csv.writer(wri)
#     cnt = 0
#     for row in reader:
#         writer.writerow(row)
#         cnt += 1
#         if cnt == 21:
#             break

repo_list = []

#选前20的pull_url
with open('repo_java_stars_top_24.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        repo_list.append([row[0], row[1]])

with open('pull_url_top_200.csv') as f, open('pull_url_top_24.csv', 'w', newline='') as wri:
    reader = csv.reader(f)
    writer = csv.writer(wri)

    for row in reader:
        url = row[0].strip()
        owner = url.split('/')[4]
        repo = url.split('/')[5]
        if [repo, owner] in repo_list:
            print(row)
            writer.writerow(row)
#构造表头

# repo_list = []
# head = ['repo_name','owner','url','stars','pull_counts','pull_comment_counts','pull_commit_counts','pull_commit_comment_counts','pull_commit_code_comment_counts']
# repo_list.append(head)
# with open('repo_java_stars_top_200.csv') as f:
#     reader = csv.reader(f)
#     for row in reader:
#         #print(row)
#         url = row[2]
#         if url != 'url':
#             for i in range(9-len(row)):
#                 row.append(0)
#             repo_list.append(row)
#
# with open('repo_java_stars_top_200.csv', 'w', newline='') as f:
#     writer = csv.writer(f)
#     for row in repo_list:
#         #print(row)
#         writer.writerow(row)
