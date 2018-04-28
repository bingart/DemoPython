#coding=utf-8
import logging
import time
import json
import random
import requests
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import stem
import stem.connection
from file_helper import FileHelper

FORMAT = '%(asctime)-15s:%(process)d: %(filename)s-%(lineno)d %(funcName)s: %(message)s'
logging.basicConfig(format=FORMAT, filename='logger.log', level=logging.DEBUG)
logging.debug('Init: %s', 'started')
logging.debug('debug message')

class TorHelper:
    
    def __init__(self, host, controlPort, socksPort, password = None):
        self._host = host
        self._controlPort = controlPort
        self._socksPort = socksPort
        self._password = password
        self._controller = Controller.from_port(address=self._host, port=self._controlPort)
        self._controller.authenticate()
        logging.debug('created, host={0}, controlPort={1}, socksPort={2}'.format(self._host, self._controlPort, self._socksPort))

    def close(self):
        self._controller.close()
            
    def getIPAddress(self) :
        proxies = {'http': 'socks5://' + self._host + ':' + str(self._socksPort)}
        resp = requests.get('http://45.79.95.201/ip.php', proxies=proxies)
        if resp.status_code == 200:
            html = resp.content.decode('utf-8')
            return html
        else:
            return "UNKNOWN"
        
    def reload(self):
        circuits = self._controller.get_circuits()
        cidList = []
        for c in circuits:
            cidList.append(c.id)    
        for cid in cidList:
            controller.close_circuit(cid)
        logging ('switch to next')
        
class TaskHelper:
    def __init__(self, taskFilePath):
        self._taskFilePath = taskFilePath
        self._taskList = FileHelper.loadFileList(self._taskFilePath)
        self._taskIndex = 0

    def getNextTask(self):
        if True:
            if len(self._taskList) == 0:
                return None
            
            url = self._taskList[self._taskIndex]
            self._taskIndex += 1
            if self._taskIndex >= len(self._taskList):
                self._taskIndex = 0
            
            taskItem = {
                'url': url,
                'action': 'scroll',
            }
            task = {
                'taskItemList': [taskItem]
            }
            return task
        else:
            # get task from service
            # TODO
            return None

class TrafficHelper:
    def __init__(self, torHelper, taskHelper, uaFilePath, torHost, torPort):
        self._torHelper = torHelperS
        self._taskHelper = taskHelper
        self._uaFilePath = uaFilePath
        self._uaList = FileHelper.loadFileList(self._uaFilePath)
        self._uaIndex = random.randint(1, len(self._uaList))
        self._torHost = torHost
        self._torPort = torPort
        
    def load(self, url):
        try:
            serviceArgs = ['--proxy=127.0.0.1:9350', '--proxy-type=socks5']
            serviceArgs += ['--load-images=no'] 
            driver = webdriver.PhantomJS('/usr/bin/phantomjs', service_args=serviceArgs)
            driver.get(url)
            html = driver.page_source
            print(html)
            
            for i in range(10):
                time.sleep(1)
                print('sleep')
        
        finally:
            driver.close()

    def invoke(self):
        task = self._taskHelper.getNextTask()
        if task == None or (not 'taskItemList' in task):
            loggin.debug('no more task, return')
            return
            
        # check all task item
        taskItemList = task['taskItemList']
        if taskItemList == None or len(taskItemList) == 0:
            loggin.debug('empty task item list, return')
            return
            
        # ip address
        self._torHelper.reload()
        ipAddress = self._torHelper.getIPAddress()
        logging.debug('pre-invoking: ipAddress={0}'.format(ipAddress))

        # load all task item
        for taskItem in taskItemList:
            url = taskItem['url']
            load(url)
            
def ipLookup():
    try:
        helper = TorHelper('127.0.0.1', 9351, 9350)
        ipAddress = helper.getIPAddress()
        print ('ipAddress={0}'.format(ipAddress))
    except Exception as err :
        print(err)
    finally:
        helper.close()

if __name__=="__main__":
    print("main")
    #ipLookup()
    print("exit")
