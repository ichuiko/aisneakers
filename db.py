import sqlite3
from datetime import datetime
import os.path as pt
import json
import random

#conn = sqlite3.connect(pt.abspath("db.db"))
#cursor = conn.cursor()
#query = """CREATE TABLE tsdne_links (id INTEGER PRIMARY KEY AUTOINCREMENT , link text )"""
#cursor.execute(query)
#query = """CREATE TABLE users (userId int PRIMARY KEY)"""
#cursor.execute(query)
#query = """CREATE TABLE posts (id text PRIMARY KEY, link text, date_create text, header text, is_parsed int, content text,  sended_to_tg int, sended_to_tg_date text, sended_to_openai int , sended_to_openai_date text, openai_content text )"""
#cursor.execute(query)
#query = """CREATE TABLE images (postId text, link text)"""
#cursor.execute(query)

def createPost(data:dict):
    conn = sqlite3.connect(pt.abspath("db.db"))
    cursor = conn.cursor()
    try:
        query = f"""INSERT INTO posts VALUES ('{data['postId']}', '{data['link']}', '{datetime.now()}', '{data['header']}',0, NULL, 0, NULL, 0, NULL, NULL)"""
        cursor.execute(query)
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False

def getNonParsedPostLinks():
    conn = sqlite3.connect(pt.abspath("db.db"))
    cursor = conn.cursor()
    query = f"""SELECT id,link FROM posts WHERE is_parsed = 0"""
    cursor.execute(query)
    items = cursor.fetchall()
    return items

def updatePost(postId:str, operation=None, data=None):
    conn = sqlite3.connect(pt.abspath("db.db"))
    cursor = conn.cursor()
    if operation == None:
        query = f"""UPDATE posts SET content= '{data['content']}', is_parsed=1 WHERE id='{postId}'"""
        cursor.execute(query)
        conn.commit()
        for img in data['images']:
            query = f"""INSERT INTO images VALUES('{postId}', '{img}')"""
            cursor.execute(query)
            conn.commit()
    elif operation == 'send_to_telegram':
        query = f"""UPDATE posts SET sended_to_tg = 1 WHERE id='{postId}'"""
        cursor.execute(query)
        conn.commit()
    elif operation == 'send_to_openai':    
        query = f"""UPDATE posts SET sended_to_openai = 1 WHERE id='{postId}'"""
        cursor.execute(query)
        conn.commit()
    return True

def getNonSendedToTGPosts():
    conn = sqlite3.connect(pt.abspath("db.db"))
    cursor = conn.cursor()
    query = f"""SELECT id,link, header FROM posts WHERE sended_to_tg = 0"""
    cursor.execute(query)
    items = cursor.fetchall()
    result = []
    for item in items:
        query = f"""SELECT link FROM images WHERE postId = '{item[0]}'"""
        cursor.execute(query)
        images = cursor.fetchall()
        data = {
            'info' : item,
            'images' : images
        }
        result.append(data)
    return result

def getPostContentById(postId:str) :
    conn = sqlite3.connect(pt.abspath("db.db"))
    cursor = conn.cursor()
    query = f"""SELECT content FROM posts WHERE id = '{postId}'"""
    cursor.execute(query)
    posts = cursor.fetchall()
    post = posts[0][0]
    request = """Mike is a famous sneaker blogger in Youtube. He likes sneakers and he giving his opinion about all sneaker news with some jokes and memes.
As Mike, write a small article about that new in russian language.
News:"""
    mainPost = json.loads(post)
    ind = mainPost.find('Read Full Article')
    content = request + mainPost[:ind]
    content += 'tl;dr'

    return content

def getImagesByPostId(postId:str) :
    conn = sqlite3.connect(pt.abspath("db.db"))
    cursor = conn.cursor()
    query = f"""SELECT link FROM images WHERE postId = '{postId}'"""
    cursor.execute(query)
    img = cursor.fetchall()
    
    return img

def saveUserId(userId:int) :
    conn = sqlite3.connect(pt.abspath("db.db"))
    cursor = conn.cursor()
    try:
        query = f"""INSERT INTO users VALUES({userId})"""
        cursor.execute(query)
        conn.commit()
    except sqlite3.IntegrityError:
        return 
    return

def getGeneratedLinks(count=10):
    conn = sqlite3.connect(pt.abspath("db.db"))
    cursor = conn.cursor()
    query = """SELECT id FROM tsdne_links"""
    cursor.execute(query)
    data = cursor.fetchall()
    max = len(data)
    result = []
    counter = 0

    while counter != count:
        index = random.randint(1,max)
        query = f"""SELECT link FROM tsdne_links WHERE id = {index}"""
        cursor.execute(query)
        link = cursor.fetchall()
        result.append(link[0][0])
        counter += 1

    return result
