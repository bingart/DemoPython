from selenium import webdriver
import time

service_args = ['--proxy=127.0.0.1:9350', '--proxy-type=socks5']
service_args += ['--load-images=no'] 

driver = webdriver.PhantomJS('/usr/bin/phantomjs', service_args=service_args)
#driver.get('http://www.infosoap.com')
driver.get('https://www.amazon.com/Cole-Haan-Womens-Emory-Wedge/dp/B079YNJYKZ/ref=pd_rhf_se_s_cp_0_2?_encoding=UTF8&pd_rd_i=B079YNJYKZ&pd_rd_r=WE2PGWYGTP3RQ3KY5XZ3&pd_rd_w=3fK7v&pd_rd_wg=MP4rO&refRID=WE2PGWYGTP3RQ3KY5XZ3')
 
html = driver.page_source
print(html)
print('len='+str(len(html)))

for i in range(10):
    time.sleep(1)
    print('sleep')

driver.close()
