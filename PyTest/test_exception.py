#coding=utf-8
#Deprecated

import logging
import time
import random
import requests
from selenium import webdriver
from stem.control import Controller
from file_helper import FileHelper

FORMAT = '%(asctime)-15s:%(process)d: %(filename)s-%(lineno)d %(funcName)s: %(message)s'
logging.basicConfig(format=FORMAT, filename='test.exception.log', level=logging.DEBUG)
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
            self._controller.close_circuit(cid)
        logging ('switch to next')
        
class TaskHelper:
    def __init__(self, taskFilePath):
        self._taskFilePath = taskFilePath
        self._taskList = FileHelper.loadFileList(self._taskFilePath)
        self._taskIndex = random.randint(1, len(self._taskList))

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
                'actionList': ['scroll 500', 'sleep 10'],
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
        self._torHelper = torHelper
        self._taskHelper = taskHelper
        self._uaFilePath = uaFilePath
        self._uaList = FileHelper.loadFileList(self._uaFilePath)
        self._uaIndex = random.randint(1, len(self._uaList))
        self._torHost = torHost
        self._torPort = torPort
        
    def load(self, url, delay):
        try:
            serviceArgs = ['--proxy=127.0.0.1:9350', '--proxy-type=socks5']
            serviceArgs += ['--load-images=no'] 
            driver = webdriver.PhantomJS('/usr/bin/phantomjs', service_args=serviceArgs)
            driver.get(url)
            html = driver.page_source
            print(html)
            
            if delay > 0:
                for i in range(delay):
                    time.sleep(1)
                    print('sleep at {0}'.format(i))
        except Exception as err :
            print(err)        
        finally:
            driver.close()

    def invoke(self):
        task = self._taskHelper.getNextTask()
        if task == None or (not 'taskItemList' in task):
            logging.debug('no more task, return')
            return
            
        # check all task item
        taskItemList = task['taskItemList']
        if taskItemList == None or len(taskItemList) == 0:
            logging.debug('empty task item list, return')
            return
            
        # ip address
        self._torHelper.reload()
        ipAddress = self._torHelper.getIPAddress()
        logging.debug('pre-invoking: ipAddress={0}'.format(ipAddress))

        # load all task item
        for taskItem in taskItemList:
            url = taskItem['url']
            self.load(url, 10)
            logging.debug('load task, url={0}'.format(url))

def testIPLookup(count = 1):
    try:
        for i in range(0, count, 1):
            helper = TorHelper('127.0.0.1', 9351, 9350)
            ipAddress = helper.getIPAddress()
            logging.debug ('index={0}, ipAddress={1}'.format(i, ipAddress))
            time.sleep(1)
    except Exception as err :
        print(err)
    finally:
        helper.close()

def testTraffic():
    try:
        torHelper = TorHelper('127.0.0.1', 9351, 9350)
        taskHelper = TaskHelper('./task.txt')
        trafficHelper = TrafficHelper(torHelper, taskHelper, './ua.txt', '127.0.0.1', 9350)
        trafficHelper.invoke()
        
    except Exception as err :
        print(err)
        logging.debug('test traffic error, {}', err)
    finally:
        torHelper.close()

if __name__=="__main__":
    print("main")
    #testIPLookup(1000)
    testTraffic()
    print("exit")
