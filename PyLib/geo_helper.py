# coding=utf-8

import maxminddb

class GeoHelper:
    
    def __init__(self, path):
        print ('created')
        self._reader = maxminddb.open_database(path)

    def close(self):
        self._reader.close()
    
    def getCountryInfo(self, ipAddress):
        geo = self._reader.get(ipAddress)
        if geo != None and 'country' in geo:
            country = geo['country']
            countryName = geo['country']['names']['en']
            countryCode = country['iso_code']
            return [countryName, countryCode]
        else:
            return [None, None]

if __name__=="__main__":
    print("main")
    helper = GeoHelper('GeoLite2-Country.mmdb')
    ip = '45.79.95.201'
    countryName, countryCode = helper.getCountryInfo(ip)
    print ('ip={0}, country name={1}, country code={2}'.format(ip, countryName, countryCode))
    print("exit")