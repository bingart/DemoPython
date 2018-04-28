# coding=utf-8
from log_helper import LogHelper
import requests
from requests.auth import HTTPBasicAuth
import json

class WPHelper:
    
    def __init__(self, host, userName, userPassword):
        LogHelper.log("created")
        self._host = host
        self._userName = userName
        self._userPassword = userPassword
        self._basicAuth = HTTPBasicAuth(self._userName, self._userPassword)
    
    def createCategory(self, name, slug, parent):
        payload = {
            "name": name,
            "slug": slug,
            "parent": parent
        }
        #print (payload)
        url = self._host + "/wp-json/wp/v2/categories"
        rsp = requests.post(url, json=payload, auth=self._basicAuth)
        statusCode = rsp.status_code
        content = rsp.text
        print (statusCode)
        print (content)
        if statusCode == 201:
            jsonObj = json.loads(content)
            return jsonObj['id']
        else:
            return None

    def deleteCategory(self, new_term_id):
        payload = {
            "id": new_term_id,
            "force": "true"
        }
        #print (payload)
        url = self._host + "/wp-json/wp/v2/categories/" + str(new_term_id)
        rsp = requests.delete(url, json=payload, auth=self._basicAuth)
        statusCode = rsp.status_code
        content = rsp.text
        print (statusCode)
        print (content)
        if statusCode == 200:
            return True
        else:
            return False

    def createTag(self, name, slug):
        payload = {
            "name": name,
            "slug": slug
        }
        #print (payload)
        url = self._host + "/wp-json/wp/v2/tags"
        rsp = requests.post(url, json=payload, auth=self._basicAuth)
        statusCode = rsp.status_code
        content = rsp.text
        print (statusCode)
        print (content)
        if statusCode == 201:
            jsonObj = json.loads(content)
            return jsonObj['id']
        else:
            return None
    
    def deleteTag(self, new_term_id):
        payload = {
            "id": new_term_id,
            "force": "true"
        }
        #print (payload)
        url = self._host + "/wp-json/wp/v2/tags/" + str(new_term_id)
        rsp = requests.delete(url, json=payload, auth=self._basicAuth)
        statusCode = rsp.status_code
        content = rsp.text
        print (statusCode)
        print (content)
        if statusCode == 200:
            return True
        else:
            return False

    def createPost(self, slug, title, content, excerpt, categories, tags):
        """ Create a new post.
        categories should be [] when empty, None cuase 403 error !!!!
        tags should be [] when empty, None cuase 403 error !!!!
        author is 1, be sure id exists.
        """
        payload = {
            "comment_status": "open",
            "ping_status": "open",
            "author": 1,
            "slug": slug,
            "title": title,
            "status": "publish",
            "content": content,
            "excerpt": excerpt,
            "categories": categories,
            "tags": tags}
        #print (payload)
        url = self._host + "/wp-json/wp/v2/posts"
        rsp = requests.post(url, json=payload, auth=self._basicAuth)
        statusCode = rsp.status_code
        content = rsp.text
        print (statusCode)
        print (content)
        if statusCode == 201:
            jsonObj = json.loads(content)
            return [jsonObj['id'], jsonObj['link']]
        else:
            return [None, None]

    def deletePost(self, new_ID):
        payload = {
            "id": new_ID,
            "force": "true"
        }
        #print (payload)
        url = self._host + "/wp-json/wp/v2/posts/" + str(new_ID)
        rsp = requests.delete(url, json=payload, auth=self._basicAuth)
        statusCode = rsp.status_code
        content = rsp.text
        print (statusCode)
        print (content)
        if statusCode == 200:
            return True
        else:
            return False
