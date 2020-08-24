import asyncio
import aiohttp
import time
import random
import csv
import logging
from queue import Queue
import json


# 日志模块
logger = logging.getLogger(__name__)
logger.setLevel(level = logging.INFO)
handler = logging.FileHandler("E:\log_commit_0620.txt")
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)


console = logging.StreamHandler()
console.setLevel(logging.INFO)

logger.addHandler(handler)
logger.addHandler(console)


#统计每个项目的内部commit的数量
start = time.time()
tasks = []

pull_commits_list = Queue()
crawing_pull_commit = []
repo_list = []

f = open('pull_url_top_24.csv')
for line in f:
    repo = line.strip()+'/commits?per_page=99&page=1'
    pull_commits_list.put(repo)


token_list = []
t = open('token2')
for line in t:
    token = line.strip()
    token_list.append(token)

async def get(session,url):
    headers = {"Authorization": "token " + token_list[random.randint(0,7)],"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36"
               }
    async with session.get(url,headers=headers) as response:
        return await response.json()

async def request(url,f):
    print(url, 'starting')
    async with aiohttp.ClientSession() as session:
        try:
            resjson = await get(session, url)
            # print(resjson)
            if isinstance(resjson, dict):
                print(resjson)
                time.sleep(800)
                raise Exception('This is the error message.')
            if resjson != []:
                json.dump(resjson, f)
                f.write('\n')
                for commit in resjson:
                    commit_url = commit['url']
                    comment_count = commit['commit']['comment_count']
                    print(commit_url, comment_count)
                    crawing_pull_commit.append([url, commit_url, comment_count])
                url1 = url.split('&page=')[0]
                url2 = url.split('&page=')[1]
                pull_commits_list.put(url1 + '&page=' + str(int(url2) + 1))
            elif resjson == []:
                logger.info(url +" success")
            else:
                logger.warning(url +' '+str(resjson))
        except Exception as e:
            if 'resjson' in locals().keys():
                logger.error(url + ' ' + str(resjson) + ' ' + str(e))
                if "Not Found" not in str(resjson) and "Repository access blocked" not in str(resjson):
                    pull_commits_list.put(url)
            else:
                pull_commits_list.put(url)

with open('E:\\pull_commit_0528', 'w+', encoding='utf-8') as f:
    count = 0
    while not pull_commits_list.empty() or count > 0:
        one = pull_commits_list.get()
        tasks.append(asyncio.ensure_future(request(one,f)))
        count += 1
        if count>=10:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(asyncio.wait(tasks))
            count = 0
            tasks = []
        elif count>0 and pull_commits_list.empty():
            loop = asyncio.get_event_loop()
            loop.run_until_complete(asyncio.wait(tasks))
            count = 0
            tasks = []

with open('repo_java_stars_top_24.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        #print(row)
        url = row[2]
        if url != 'url':
            row[6] = 0   #pull_commit_counts
            row[7] = 0   #pull_commit_comment_counts
        repo_list.append(row)

for commit in crawing_pull_commit:
    commit_url = commit[1]
    comment_count = commit[2]
    owner = commit_url.split('/')[4]
    repo = commit_url.split('/')[5]
    for row in repo_list:
        if owner == row[1] and repo == row[0]:
            row[6] += 1
            row[7] += comment_count
            break

with open('repo_java_stars_top_24.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    for row in repo_list:
        #print(row)
        writer.writerow(row)

with open('pull_commit_url_top_24.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    for commit in crawing_pull_commit:
        writer.writerow(commit)



