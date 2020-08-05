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


#统计每个项目的pull_request的数量
start = time.time()
tasks = []
pulls_list = Queue()

crawing_pull = []
repo_list = []

with open('repo_java_stars_top_24.csv') as f:
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
t = open('token2')
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
            if isinstance(resjson, dict):
                print(resjson)
                time.sleep(800)
                raise Exception('This is the error message.')
            if resjson != []:
                print(resjson)
                json.dump(resjson, f)
                f.write('\n')
                url1 = url.split('&page=')[0]
                url2 = url.split('&page=')[1]
                pulls_list.put(url1 + '&page=' + str(int(url2) + 1))
            elif resjson == []:
                logger.info(url + " success")
            else:
                logger.warning(url + ' ' + str(resjson))
        except Exception as e:
            if 'resjson' in locals().keys():
                logger.error(url + ' ' + str(resjson) + ' ' + str(e))
                if "Not Found" not in str(resjson) and "Repository access blocked" not in str(resjson):
                    pulls_list.put(url)
            else:
                pulls_list.put(url)


with open('F:\\pulls_0714', 'w+', encoding='utf-8') as f:
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

