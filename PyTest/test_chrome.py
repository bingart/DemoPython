import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--headless") # Runs Chrome in headless mode.
options.add_argument('--no-sandbox') # # Bypass OS security model
options.add_argument('start-maximized')
options.add_argument('disable-infobars')
options.add_argument("--disable-extensions")
options.add_argument("user-agent=curl.useragent")
options.add_argument("--proxy-server=socks5://{0}:{1}".format("localhost", 9350));
options.add_argument("window-size=1050,800")
driver = webdriver.Chrome(chrome_options=options, executable_path='/root/chromedriver')
pid = driver.service.process.pid
print('open driver, pid={0}'.format(pid))
driver.set_window_size(414, 736)
driver.get("http://www.infosoap.com")
print ("Headless Chrome Initialized on Linux OS")
print(driver.title)
for i in range(0, 10):
    time.sleep(1)

driver.quit()

