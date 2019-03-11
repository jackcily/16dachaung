> windows下获取一个动态网页的所有href链接

```python

# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import unittest, time, os
import re
import io

prefs = {"download.default_directory": "E:\download","download.prompt_for_download": False,}

chrome_options = Options()
chrome_options.add_experimental_option("prefs", prefs)
chrome_options.add_argument("--headless")   #设置浏览器运行状态为无头模式
#windowa 下chromedriver的安装路径
path = 'C:/Program Files (x86)/Google/Chrome/Application/chromedriver.exe'
browser = webdriver.Chrome(path,chrome_options=chrome_options)

start_url = "http://samr.cfda.gov.cn/WS01/CL1688/237674.html"

try:
    browser.get(start_url)
except TimeoutError:
    print("time too long")


# 使用xpath直接获取所有的href标签
#然后根据对应的text 内容是否包含合格 不合格标签 以及链接的最后是够是 xls 标签决定是否需要下载
#如果合格就下载 否则不存储到队列中
list_href = []
list_text =[]
for link in browser.find_elements_by_xpath("//*[@href]"): #定位本页面中的所有 href标签
    if(re.match(".*\.xls",link.get_attribute('href'))):   #判断href的链接是不是包含 .xsl  如果是才需要下载
        #print(link.get_attribute('href'))
        list_text.append(link.text)
        list_href.append(link.get_attribute('href'))


for i in range(len(list_text)):
    print(list_text[i]+" "+list_href[i])


```



- [ ] todo 

  获得了下载链接发现使用 driver.get(download_url) ，只能获得一个包含js代码的网页，并不能真的获得对应的xls文件。
