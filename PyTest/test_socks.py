from selenium import webdriver
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

#path to TOR binary
binary = FirefoxBinary(r'C:\Users\j-sunfei\Desktop\Tor Browser\Browser\firefox.exe')
#path to TOR profile
profile = FirefoxProfile(r'C:\Users\j-sunfei\Desktop\Tor Browser\Browser\TorBrowser\Data\Browser\profile.default')

profile = webdriver.FirefoxProfile()
profile.set_preference('network.proxy.type', 1)
profile.set_preference('network.proxy.socks', '127.0.0.1')
profile.set_preference('network.proxy.socks_port', 9150)

#driver = webdriver.Firefox(firefox_profile= profile, firefox_binary= binary)
driver = webdriver.Firefox(firefox_binary= binary)
driver.get("http://icanhazip.com")
driver.save_screenshot("screenshot.png")
driver.quit()