# coding=utf-8

import datetime
import pytz
 
def tz2ntz(date_obj, tz, ntz):
    """
    :param date_obj: datetime object
    :param tz: old timezone
    :param ntz: new timezone
    """
    if isinstance(date_obj, datetime.date) and tz and ntz:
       date_obj = date_obj.replace(tzinfo=pytz.timezone(tz))
       return date_obj.astimezone(pytz.timezone(ntz))
    return False

if __name__=="__main__":
    print("main")
    now = datetime.datetime.utcnow()
    newDt = tz2ntz(now, 'UTC', 'US/Pacific')    
    print(now)
    print(newDt)

    now = datetime.datetime.now()
    print(now)
    
    docList = []
    
    doc1 = {'a': 'aa'}
    doc2 = {'b': 'bb'}
    doc3 = {'c': 'cc'}
    
    docList.append(doc1)
    docList.append(doc2)
    docList.append(doc3)
    
    doc2['b'] = 'bbb'
    
    docList.remove(doc2)
    print (docList)
