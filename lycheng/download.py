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
prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': 'E:\\download'}

# 设置浏览器的相关配置
chrome_options = Options()
chrome_options.add_experimental_option('prefs', prefs)
# chrome_options.add_argument("--headless")

browser = webdriver.Chrome(chrome_options=chrome_options)

# 存储抽检报告的网址
thecheckannouncement = []


def dowload(start_url):

    # 如果发送网页请求时间过长的情况
    try:
        browser.get(start_url)
    except TimeoutError:
        print("Time Out，try again")
        browser.get(start_url)

    # 打印网页源码,并进行保存
    # print(browser.page_source)
    # with open("E:\download\\test.txt", "w", encoding='utf-8') as f:
    #     f.write(browser.page_source)
    #     f.close()

    # 定位下载元素，检查下载元素的文本提示信息中是否还有关键字
    if browser.find_elements(By.PARTIAL_LINK_TEXT, "不合格") != []:
        print("查询到有相关内容的食品抽检不合格报告")
        all_dowload = browser.find_elements(By.PARTIAL_LINK_TEXT, "不合格")
        time.sleep(1)
        for i in all_dowload:
            try:
                if "小知识" not in i.text:
                    print("%s" % (i.text), end=" ")
                    print(i.get_attribute("href"))
                    browser.get(i.get_attribute("href"))
            except:
                pass
    else:
        print("该页面没有这个找到这个元素")


# 获得所有报告的下载地址
def getReportUrl(start_url):

    # 如果发送网页请求时间过长的情况
    try:
        browser.get(start_url)
    except TimeoutError:
        print("Time Out，try again")
        browser.get(start_url)

    # 定位“下一页”按钮
    nextpageurl = browser.find_elements(By.CLASS_NAME, "pageTde15")[0].find_elements(By.PARTIAL_LINK_TEXT, "")[
        0].get_attribute("href")

    while (True):
        # 获得抽检公共信息
        linkinfo = browser.find_elements(By.CLASS_NAME, "ListColumnClass15")

        for link in linkinfo:
            thecheckannouncement.append(
                [link.text, link.find_elements(By.PARTIAL_LINK_TEXT, "")[0].get_attribute("href")])

        # 访问下一页
        browser.get(nextpageurl)
        time.sleep(1)
        nextpageurl = browser.find_elements(By.CLASS_NAME, "pageTde15")[0].find_elements(By.PARTIAL_LINK_TEXT, "")[
            0].get_attribute("href")

        # 但下一页网址与当前网址相同，说明已经到达最后一页
        if browser.current_url == nextpageurl:
            break

if __name__ == '__main__':
    # 该爬虫只针对 http://samr.cfda.gov.cn/WS01/CL1664 下的抽检报告网页
    start_url = "http://samr.cfda.gov.cn/WS01/CL1664/index.html"
    # 获得所有抽检报告的网址
    getReportUrl(start_url)
    # 下载有提到不合格的.xls
    for i in thecheckannouncement:
        dowload(i[1])
