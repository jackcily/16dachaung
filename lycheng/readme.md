# webdriver 相关

## 运行环境

- python 3

- selenium库

- webdriver

    - selenium默认支持Firefox
        
    - chrome和IE相关webdriver得自行下载，下载时请注意webdriver版本需与浏览器版本对应。

    - [webdriver下载地址(需翻墙)](http://chromedriver.storage.googleapis.com/index.html)

- 服务器环境已经部署成功

## 爬虫说明

- 爬取[该网站](http://samr.cfda.gov.cn/WS01/CL1664/)下的所有抽检报告，共8331条

- 爬取过程

    1. 相关网页共416页，先将每一页上的各省抽检报告链接爬取(共8331条)

    2. 挨个访问各省抽检报告链接，检查该页可供下载的文件中是否有包含“不合格”字样的文件，如果有则进行下载

- 问题

    1. 部分省份抽检报告是以文字字样给出的，没有提供可下载的链接，所以这部分的抽检报告无法爬取
