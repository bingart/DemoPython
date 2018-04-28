# coding=utf-8

from user_agents import parse

def queryUserAgent():
    ua_string = 'Mozilla/5.0 (iPhone; CPU iPhone OS 5_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9B179 Safari/7534.48.3'
    user_agent = parse(ua_string)
    print('browser---')
    print(user_agent.browser) # returns Browser(family=u'Mobile Safari', version=(5, 1), version_string='5.1')
    print(user_agent.browser.family) # returns 'Mobile Safari'
    print(user_agent.browser.version) # returns (5, 1)
    print(user_agent.browser.version_string) # returns '5.1'
    print('os---')
    print(user_agent.os.family)
    print(user_agent.os.version)
    print('device---')
    print(user_agent.device.family)
    print(user_agent.device.brand)
    print(user_agent.device.model)
    print('is---')
    print(user_agent.is_mobile)
    print(user_agent.is_tablet)
    print(user_agent.is_pc)
    print(user_agent.is_touch_capable)
    print(user_agent.is_bot)

if __name__=="__main__":
    print("main")
    
    queryUserAgent()
    
    print("exit")