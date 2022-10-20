import subprocess
import time
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from tqdm import tqdm
import os
import csv

# 控制tcpdump抓包
devnull = open(os.devnull, "w")

def startTcpdump(pcapFile, logFile):
    cmd = 'tcpdump -nn -c 100 host 45.78.21.211 -w {}'.format(pcapFile)
    with open(logFile, 'w') as fi: 
        return subprocess.Popen(cmd, stdout=fi, stderr= fi, shell=True)

def killTcpdump(command):
    proc = subprocess.Popen(command, stdout=devnull, stderr=subprocess.STDOUT)
    proc.wait()
    proc.terminate()

# 浏览器设置
options = webdriver.ChromeOptions()
proxy = "socks5://127.0.0.1:2080"
options.add_argument("proxy-server={}".format(proxy))
options.add_argument("--headless")
driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), chrome_options=options)
driver.set_page_load_timeout(20)
driver.set_script_timeout(20)
proxy_type = "ss"

# 获取目标网站
sites = []
csv_reader = csv.reader(open("/Users/wbaup/242/crawler/top-1m.csv"))
for line in csv_reader:
    sites.append(line[1])

# 开始爬虫
print("start selenium")
for index in range(1000):
    
    site = sites[index]
    site = r"https://" + site
    print("get {} site : {}".format(index+1, site))
    try:
        if index % 100 == 0:
            driver.refresh()
            driver.delete_all_cookies()
    except:
        pass
    flag = False
    siteFlag = site[8:]
    pcapFile = "/Users/wbaup/242/crawler/traffic/{0}/{1}.pcap".format(proxy_type, siteFlag)
    logFile = "/Users/wbaup/242/crawler/logs/tcpdump.log"
    try:
        proc = startTcpdump(pcapFile, logFile)
        driver.get(site)
    except:
        pass
    finally:
        proc.terminate()
        cmd = "pkill tcpdump"
        killTcpdump(cmd.split(' '))
driver.quit()