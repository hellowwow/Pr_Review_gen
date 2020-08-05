import asyncio
import aiohttp
import json
import time
import random
import csv
from queue import Queue

#统计每个项目的pull_request的数量
start = time.time()
tasks = []
pulls_list = Queue()

crawing_pull = []
repo_list = []

with open('repo_java_stars_top_200.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        #print(row)
        url = row[2]
        if url != 'url':
            row[4] = 0
            pull_url = url.strip() + '/pulls?state=closed&per_page=99&page=1'
            pulls_list.put(pull_url)
        repo_list.append(row)


token_list = []
t = open('token')
for line in t:
    token = line.strip()
    token_list.append(token)

async def get(session,url):
    headers = {"Authorization": "token " + token_list[random.randint(0,7)],"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36"
               }
    async with session.get(url,headers=headers) as response:
        return await response.json()

async def request(url):
    print(url, 'starting')
    async with aiohttp.ClientSession() as session:
        try:
            resjson = await get(session, url)
            if resjson != []:
                json.dump(resjson, f)
                f.write('\n')
                for pull in resjson:
                    pull_url = pull['url']
                    print(pull_url)
                    crawing_pull.append(pull_url)
                url1 = url.split('&page=')[0]
                url2 = url.split('&page=')[1]
                pulls_list.put(url1 + '&page=' + str(int(url2) + 1))

            elif resjson == []:
                #print(123123)
                print(url + " success")

        except Exception as e:
            if 'resjson' in locals().keys():
                if "Not Found" not in str(resjson) and "Repository access blocked" not in str(resjson):
                    pulls_list.put(url)
            else:
                pulls_list.put(url)



with open('E:\\pulls_0517', 'w+', encoding='utf-8') as f:
    count = 0
    while not pulls_list.empty() or count >0 :
        one = pulls_list.get()
        tasks.append(asyncio.ensure_future(request(one)))
        count += 1
        if count>=10 :
            loop = asyncio.get_event_loop()
            loop.run_until_complete(asyncio.wait(tasks))
            count = 0
            tasks = []
        elif count>0 and pulls_list.empty():
            loop = asyncio.get_event_loop()
            loop.run_until_complete(asyncio.wait(tasks))
            count = 0
            tasks = []

for pull_url in crawing_pull:
    owner = pull_url.split('/')[4]
    repo = pull_url.split('/')[5]
    for row in repo_list:
        if owner == row[1] and repo == row[0]:
            row[4] += 1
            break


with open('repo_java_stars_top_200.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    for row in repo_list:
        print(row)
        writer.writerow(row)

with open('pull_url_top_200.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    for pull_url in crawing_pull:
        writer.writerow([pull_url])


# pull = "https://api.github.com/repos/octocat/Spoon-Knife/pulls/20242"
# owner = pull.split('/')[4]
# repo = pull.split('/')[5]
# print(owner, repo)