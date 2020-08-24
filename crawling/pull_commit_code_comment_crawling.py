# from urllib.request import urlopen
# from urllib.request import Request
# import json
# import csv
#
# def get_results(url, headers):
#     #https://api.github.com/search/repositories?q=java+stars%3A>10000&sort=stars
#     req = Request(url,headers=headers)
#     response = urlopen(req).read()
#     result = json.loads(response.decode())
#     return result
#
# if __name__ == '__main__':
#     #58ad091363dd6a8f84578f8a5fa0ad84c3607b29
#     headers = {'User-Agent': 'Mozilla/5.0',
#                'Authorization': 'token 58ad091363dd6a8f84578f8a5fa0ad84c3607b29',
#                'Content-Type': 'application/json',
#                'Accept': 'application/json'
#                }
#     #results = get_results(headers)
#
#     #获得项目url
#     review_url_list = []
#     with open('review_comments_url.csv') as f:
#         reader = csv.reader(f)
#         for row in reader:
#             #print(row)
#             review_url = row[1]
#             review_url_list.append(review_url)
#
#     #获取review
#     with open('review_data', 'w') as f:
#         for review_url in review_url_list:
#             print(review_url)
#             results = get_results(review_url, headers)
#             for review in results:
#                 print(review)
#                 json.dump(review, f)
#                 f.write('\n')
#         # review_url = 'https://api.github.com/repos/airbnb/javascript/pulls/2201/comments'
#         # print(review_url)
#         # results = get_results(review_url, headers)
#         # for review in results:
#         #     print(review)
#         #     json.dump(review, f)
#         #     f.write('\n')






import asyncio
import aiohttp
import time
import random
import datetime
import json
import logging
from queue import Queue

# time.sleep(7200)

#日志模块
logger = logging.getLogger(__name__)
logger.setLevel(level = logging.INFO)
handler = logging.FileHandler("E:\\log_review_0428.txt")
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)


console = logging.StreamHandler()
console.setLevel(logging.INFO)

logger.addHandler(handler)
logger.addHandler(console)



start = time.time()
tasks = []
review_url_list = Queue()

f = open('pull_url_top_200.csv') # repo_list
for line in f:
    url = line.strip()+'/comments?per_page=99&page=1'
    review_url_list.put(url)


# temp_cnt = 10
# f = open('review_comments_url.csv') # repo_list
# for line in f:
#     if temp_cnt >= 0:
#         temp_cnt -= 1
#         repo = line.strip()+'?per_page=99&page=1'
#         review_url_list.put(repo)


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


async def request(url, f):
    now_time = datetime.datetime.now()
    logger.info(url + " start...")
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
                url1 = url.split('&page=')[0]
                url2 = url.split('&page=')[1]
                review_url_list.put(url1 + '&page=' + str(int(url2) + 1))
            elif resjson == []:
                logger.info(url + " success")
            else:
                logger.warning(url + ' ' + str(resjson))
        except Exception as e:
            if 'resjson' in locals().keys():
                logger.error(url + ' ' + str(resjson) + ' ' + str(e))
                if "Not Found" not in str(resjson) and "Repository access blocked" not in str(resjson):
                    review_url_list.put(url)
            else:
                review_url_list.put(url)

with open('E:\\pull_commit_code_comment_0525', 'w+', encoding='utf-8') as f:
    count = 0
    while not review_url_list.empty() or count >0 :
        one = review_url_list.get()
        tasks.append(asyncio.ensure_future(request(one,f)))
        count += 1
        if count>=10 :
            loop = asyncio.get_event_loop()
            loop.run_until_complete(asyncio.wait(tasks))
            count = 0
            tasks = []
        elif count>0 and review_url_list.empty():
            loop = asyncio.get_event_loop()
            loop.run_until_complete(asyncio.wait(tasks))
            count = 0
            tasks = []
