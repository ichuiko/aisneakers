import requests
import json
from bs4 import BeautifulSoup
import os.path as pt
from datetime import datetime
from db import createPost, getNonParsedPostLinks, updatePost , getNonSendedToTGPosts

class Hypebeast() :
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
    }

    def getListOfPosts(self):
        #returns 5 last posts
        url = 'https://hypebeast.com/footwear'
        html = requests.get(url, headers=self.headers)
        html.encoding = 'utf-8'
        result = []
        if html.status_code == 200:
            soup = BeautifulSoup(html.text, 'lxml')
            posts_box = soup.find('div', class_='posts')
            posts = posts_box.find_all('div', class_='post-box')
            for post in posts:
                data = {
                    'link' : post['data-permalink'],
                    'postId' : post['id'],
                    'header' : json.dumps(post['data-title'].replace("'","")),
                }
                result.append(data)
            return result
        else:
            return None
    
    def getPostInfoByLink(self, link:str) :
        html = requests.get(link, headers=self.headers)
        html.encoding = 'utf-8'
        if html.status_code == 200:
            soup = BeautifulSoup(html.text, 'lxml')
            content = soup.find('div', class_='post-body-content')
            text = content.get_text()
            images = []
            imgBlock = soup.find('div', class_='hb-gallery')
            imgData = json.loads(imgBlock['data-images'])
            for img in imgData:
                images.append(img['src'])
            result = {
                'content' : json.dumps(text.replace("'","" )),
                'images' : images
            }

            return result
        
    def parse(self) :
        info = self.getListOfPosts()
        if info != None :
            for item in info:
                a = createPost(item)

        postsToParse = getNonParsedPostLinks()
        for post in postsToParse:
            print(post)
            info = self.getPostInfoByLink(post[1])
            updatePost(data=info,postId=post[0])

if __name__ == "__main__" :
    app = Hypebeast()
    app.parse()