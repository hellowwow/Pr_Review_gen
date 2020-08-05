


import requests
import json
import csv
headers = {'User-Agent': 'Mozilla/5.0',
               'Authorization': 'token 58ad091363dd6a8f84578f8a5fa0ad84c3607b29',
               'Content-Type': 'application/json',
               'Accept': 'application/json'
               }

def jsondump():
    with open('repo_java_stars_7000.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        head = ['name', 'owner', 'url', 'stars']
        writer.writerow(head)
        for i in range(1, 4):
            url = 'https://api.github.com/search/repositories?q=language%3Ajava+stars%3A>7000&per_page=99&page=' + str(i)
            print(url)
            results = requests.get(url,headers = headers)
            print(results)
            results = results.json()
            print(results['total_count'])
            for item in results['items']:
                name = item['name']
                owner = item['owner']['login']
                url = item['url']
                stars = item['stargazers_count']
                print(name, owner, url, stars)
                writer.writerow([name, owner, url, stars])

jsondump()