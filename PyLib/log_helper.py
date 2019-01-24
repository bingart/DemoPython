# coding=utf-8

import logging

class LogHelper:
    
    @staticmethod
    def init(logFilePath, isStdout = True):
        logHandlers = [
            logging.FileHandler(logFilePath)
        ]
        if isStdout:
            logHandlers.append(logging.StreamHandler())
            
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s %(filename)s[line:%(lineno)d] [%(levelname)s] %(message)s",
            handlers = logHandlers   
        )
