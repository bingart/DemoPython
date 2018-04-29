# coding=utf-8
import time
import os
import re
import sys
import json
from datetime import datetime
from pymongo import MongoClient
from bs4 import BeautifulSoup
from http_helper import HttpHelper
from mongo_helper import MongoHelper
from url_helper import UrlHelper
from str_helper import StrHelper
from nlp_helper import NLPHelper
from crypt_helper import CryptHelper
from doc_helper import DocHelper

DISPATCHER_URL = "http://dispatcher.9in.com:8088"
IMPORT_URL = "http://localhost:54691/DataImport/Article"
IMPORT_URL = "https://www.popular123.com/DataImport/Article"

def getTask():
    try: 
        req = {
            'uid': 'NET_0',
            'whiteList': ['article']
        }
        errorCode, rsp = HttpHelper.post(DISPATCHER_URL + "/webapi/task2", req)
        if rsp != None and 'errorCode' in rsp and rsp['errorCode'] == 'OK' and 'taskList' in rsp and rsp['taskList'] != None:
            task = rsp['taskList'][0]
            print ("get task ok, task=" + json.dumps(task))
            return ['OK', task]
        else:
            print ("get task error, rsp=" + json.dumps(rsp))
            return [rsp['errorCode'], None]
        
    except Exception as err :
        print(err)
        return ['UNKNOWN', None]

def parseAndImport(url, html):
    md5 = CryptHelper.getMD5Hash(url)
    if html != None and len(html) > 0:
        found, doc = DocHelper.parseDoc(html)
        article, errorCode = DocHelper.doc2Article(doc, url)
        if errorCode != "OK" or article == None:
            article = {
                'id': md5,
                'status': article['status'],
            }
    else:
        if len(url) >= 1000:
            url = url[0:1000]
        article = {
            'id': md5,
            'status': article['status'],
        }

    articleList = []
    articleDoc = {
        'id': article['md5'],
        'title': article['title'],
        'excerpt': article['excerpt'],
        'content': article['content'],
        'author': article['author'],
        'domain': article['domain'],
        'categories': article['categories'],
        'tags': article['tags'],
        'url': article['url'],
        'status': article['status'],
        'key': article['key'],
    }
    articleList.append(articleDoc)
    errorCode, rsp = HttpHelper.post(IMPORT_URL, articleList)
    if errorCode == "OK" and rsp != None and 'isOk' in rsp and rsp['isOk'] == True:
        print ("import article ok, id=" + article['md5'])
    else:
        print ("import article error, id=" + article['md5'])

def fetchTask(task):
    try: 
        url = task['url']
        statusCode, html = HttpHelper.fetch(url)
        if html != None and len(html) > 0:
            print ("fetch task ok")
        else:
            print ("fetch task error")
        
        # parse and update    
        parseAndImport(url, html)
        
    except Exception as err :
        print(err)

def completeTask(task):
    try: 
        req = {
            'uid': 'NET_0',
            'task': task
        }
        errorCode, rsp = HttpHelper.post(DISPATCHER_URL + "/webapi/complete2", req)
        if rsp != None and 'errorCode' in rsp and rsp['errorCode'] == 'OK':
            print ("complete task ok, task=" + json.dumps(task))
        else:
            print ("complete task error, rsp=" + json.dumps(rsp))
    except Exception as err :
        print(err)

if __name__=="__main__":
    print("main")
    for index in range(0, 1000, 1):
        errorCode, t = getTask()
        if errorCode == "NO_MORE_TASK":
            break
        elif errorCode == "OK" and t != None:
            fetchTask(t)
            completeTask(t)
        else:
            time.sleep(1)
    print("exit")