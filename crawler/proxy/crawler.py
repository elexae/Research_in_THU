from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


options = webdriver.ChromeOptions()
#proxy = "socks5://127.0.0.1:1084"
#options.add_argument("proxy-server={}".format(proxy))
#options.add_argument("--headless")
browser = webdriver.Remote(
    command_executor='http://127.0.0.1:4448/wd/hub',
    desired_capabilities=DesiredCapabilities.CHROME,
    #options = options,
)

browser.get("https://google.com")
browser.save_screenshot("google.png")