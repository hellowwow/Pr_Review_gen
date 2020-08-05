import asyncio
import aiohttp
import time
import random
import datetime
import json
import logging
from queue import Queue

index = 2
qujian = 50000

#日志模块
logger = logging.getLogger(__name__)
logger.setLevel(level = logging.INFO)
handler = logging.FileHandler("F:\\log_review_0528.txt")
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)


console = logging.StreamHandler()
console.setLevel(logging.INFO)

logger.addHandler(handler)
logger.addHandler(console)



start = time.time()
tasks = []
pull_comment_url_list = Queue()

cnt_now = 0
f = open('pull_url_top_24.csv') # repo_list
for line in f:
    repo, pull_id = line.strip().split('/pulls/')
    pull_comment_url = repo + '/issues/' + pull_id + '/comments' + '?per_page=99&page=1'
    # print(pull_comment_url)
    if cnt_now >= (index - 1) * qujian and cnt_now <= index * qujian:
        pull_comment_url_list.put(pull_comment_url)
    cnt_now += 1

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


async def request(url, f):
    now_time = datetime.datetime.now()
    logger.info(url + " start...")
    async with aiohttp.ClientSession() as session:
        try:
            resjson = await get(session, url)
            print(resjson)
            if isinstance(resjson, dict):
                print(resjson)
                time.sleep(800)
                raise Exception('This is the error message.')
            if resjson != []:
                json.dump(resjson, f)
                f.write('\n')
                url1 = url.split('&page=')[0]
                url2 = url.split('&page=')[1]
                pull_comment_url_list.put(url1 + '&page=' + str(int(url2) + 1))
            elif resjson == []:
                logger.info(url + " success")
            else:
                logger.warning(url + ' ' + str(resjson))
        except Exception as e:
            if 'resjson' in locals().keys():
                logger.error(url + ' ' + str(resjson) + ' ' + str(e))
                if "Not Found" not in str(resjson) and "Repository access blocked" not in str(resjson):
                    pull_comment_url_list.put(url)
            else:
                pull_comment_url_list.put(url)

with open('F:\\pull_comment_0528_' + str(index), 'w+', encoding='utf-8') as f:
    count = 0
    while not pull_comment_url_list.empty() or count >0 :
        one = pull_comment_url_list.get()
        tasks.append(asyncio.ensure_future(request(one,f)))
        count += 1
        if count>=10 :
            loop = asyncio.get_event_loop()
            loop.run_until_complete(asyncio.wait(tasks))
            count = 0
            tasks = []
        elif count>0 and pull_comment_url_list.empty():
            loop = asyncio.get_event_loop()
            loop.run_until_complete(asyncio.wait(tasks))
            count = 0
            tasks = []
