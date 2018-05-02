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
logging.basicConfig(format=FORMAT, filename='test_exception.log', level=logging.DEBUG)
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
        logging.debug ('reload')
    
    def dump(self):
        logging.debug("running version %s" % self._controller.get_version())
        logging.debug("running pid %s" % self._controller.get_pid())
        
        circuits = self._controller.get_circuits()
        logging.debug('circuits=%d' % len(circuits))
        for c in circuits:
            logging.debug('c: id={0}, status={1}, path={2}, purpose={3}'.format(c.id, c.status, c.path, c.purpose))
            path = '{0}'.format(c.purpose)
            for nodeItem in c.path:
                logging.debug ('nodeItem={0}'.format(nodeItem))
                path += ';' + nodeItem[0] + ',' + nodeItem[1]
            logging.debug('c.path={0}'.format(path))
                
        streams = self._controller.get_streams()
        logging.debug('streams=%d' % len(streams))
        for s in streams:
            logging.debug('s: id={0}, circ_id={1}, source_address={2}, target_address={3}'.format(s.id, s.circ_id, s.source_address, s.target_address))
    
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
            logging.debug('html.len={0}, html={1}'.format(len(html), html[0, 16]))
            
            if delay > 0:
                for i in range(delay):
                    time.sleep(1)
                    logging.debug('sleep at {0}'.format(i))
        except Exception as err :
            print(err)
            logging.debug('load exception, {0}'.format(err))        
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
        helper = TorHelper('127.0.0.1', 9351, 9350)
        for i in range(0, count, 1):
            helper.reload()
            logging.debug ('index={0}, reload'.format(i))
            ipAddress = helper.getIPAddress()
            logging.debug ('index={0}, ipAddress={1}'.format(i, ipAddress))
            helper.dump()
            time.sleep(5)
    except Exception as err :
        print(err)
        logging.debug('testIPLookup exception, {0}'.format(err))        
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
        logging.debug('test traffic error, {0}'.format(err))
    finally:
        torHelper.close()

if __name__=="__main__":
    print("main")
    testIPLookup(20000)
    #testTraffic()
    print("exit")
