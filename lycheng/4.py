# 相关库的调用可直接使用pycharm中的库管理工具下载，但selenium库只支持
# firefox的直接使用，如果使用其他浏览器的话，需要下载对应的浏览器内核，
# 比如chromedriver。但不同的浏览器版本对应不同的浏览器内核，下载的时候
# 需要下载对应的内核版本。下载完成后需要配置环境变量，并把文件放在浏览器
# 安装目录下面

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import unittest, time, os

# 指定下载的路径
prefs = {"download.default_directory": "E:\download","download.prompt_for_download": False,}

# 设置浏览器的相关配置，以无前端模式运行
chrome_options = Options()
chrome_options.add_experimental_option("prefs", prefs)
chrome_options.add_argument("--headless")

browser = webdriver.Chrome(chrome_options=chrome_options)

start_url = "http://samr.cfda.gov.cn/WS01/CL1688/237674.html"

# 如果发送网页请求时间过长的情况
try:
    browser.get(start_url)
except TimeoutError:
    print("Time Out，try again")
    browser.get(start_url)

# 打印网页源码,并进行保存
print(browser.page_source)
with open("test.txt", "w", encoding='utf-8') as f:
    f.write(browser.page_source)

#定位下载元素，检查下载元素的文本提示信息中是否还有关键字
if browser.find_elements(By.PARTIAL_LINK_TEXT,"不合格") != []:
    print("查询到有相关内容的食品抽检不合格报告")
    all_dowload = browser.find_elements(By.PARTIAL_LINK_TEXT,"不合格")
    time.sleep(5)
    for i in all_dowload:
        if "小知识" not in i.text:
            print("%s"%(i.text),end=" ")
            print(i.get_attribute("href"))
else:
    print("该页面没有这个找到这个元素")
