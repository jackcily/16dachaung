> 　使用 Selenium爬取网页

- [ ] 使用selenuim爬取指定url，代码如下：

  ```python
  
  #coding=utf-8
  import io
  from selenium import webdriver
  from pyvirtualdisplay import Display
  
  if __name__ == '__main__':
      display = Display(visible=0, size=(800, 800))
      display.start()
      browser = webdriver.Chrome()
      browser.get('http://samr.cfda.gov.cn/WS01/CL1688/239589.html')
      #print (browser.title)
      #page = browser.page_source
      #print(type(page))
      #print(page)
      with io.open("test.txt", "w",encoding = 'utf-8') as f:
          f.write(browser.page_source)
  
  
  ```

- [ ] 文件爬取以后会存储在`test.txt`中，使用putty配套软件[pscp.exe](https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html)将服务器上的文件下载到本地

  - 首先下载 pscp.exe软件。

  - 在cmd窗口中切换到含有 pscp.exe的目录中，输入 pscp 验证该软件是否可用 ，使用pscp下载服务器上的指定文件。

    ```python
    
    命令解释：
       格式:  pscp -i 认证秘钥路径  用户名@服务器:需要下载的文件的路径 本地存储的文件夹
       示例：  pscp -i F:\学习资料\aaa大三上\dachuang\dachuang_log\SSH_key1.ppk ubuntu@62.234.117.231:/home/test.txt F:\test
                
       因为本服务器的key的登录用户只能是ubuntu，所以用户只能使用 ubuntu 进行登录。
    
       因为各用户的子文件夹没有设置读写执行的权限，所以如果服务器上的文件必须放在ubuntu的子文件中，否则访问会被拒绝（因为当前登录用户是ubuntu)
        
    
    
    ```

- [ ]  **todo**

   将文件成功下载到本地以后会发现中文全部乱码，因为该网页的默认编码是`gb2312` 而在python中全部被存储成了`utf-8`