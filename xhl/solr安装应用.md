[TOC]



----

##### 名词解释

- 垂直搜索

  垂直搜索和普通的网页搜索的最大区别是对网页信息进行了结构化信息抽取加工，也就是将
  网页的非结构化数据抽取成特定的结构化信息数据.

  垂直搜索的结构化信息提取和加工主要包括：网页元数据的提取和内容中结构化实体信息的提取。这些数据存储到数据库中，进行进一步的加工处理，如：去重、分类等，最后分词、索引再以搜索的方式满足用户的需求。目前，大部分垂直搜索的结构化信息提取都是依靠手工、半手工的方式来完成的，面对互联网的海量信息，很难保证信息的实时性和有效性，因此智能化成为垂直搜索的发展趋势。

  

- solr各种名词解释

  - collection

    集合 我理解为数据的意思

  - configSet

    是 core 的配置文件 其中包括`schema.xml`和`solrconfig.xml`两个配置文件

    数据集合选用不同的configSet 就会被配置上不同的文件。

  - solrconfig.xml

    solrconfig.xml文件是solr的主配置文件。

  - schema.xml

    文件主要配置`索引和查询`的字段信息，定义了所有的数据类型和各索引字段的信息（如类型，是否建立索引，是否存储原始信息等）

  - core

    一个core就像一个实例一样  一个服务器下可以有多个实例，每个实例下都有自己的索引库和与之相应的配置文件，所以在操作solr创建索引之前需要创建一个core，因为建立索引需要配置文件，索引存储在core下面

  - jetty

    **todo**

    

----

##### solr 安装

- 安装环境 

  ubuntu16.04 + solr7.6

- 首先下载安装solr ，此处选用solr7.7

- 启动solr服务 (此后**默认工作目录在solr的安装目录**下)

  ```bash
  #进入solr的安装目录
  cd /usr/local/solr-7.7.1/
  
  #启动solr   默认启动时8983端口
  bin/solr start
  ```

- 新建core

- 将`example/example-DIH/solr/solr`文件夹中的conf文件夹和core.properties文件copy到已经新建好的core的目录。

- 重启solr

  

  

---

##### 配置中文分词器 IK-Analyzer-Solr7

- 首先在github上下载安装包 [ik-analyzer-solr7](https://github.com/magese/ik-analyzer-solr7)

- 将下载好的jar数据包放在 `/usr/local/solr-7.7.1/server/solr-webapp/webapp/WEB-INF/lib` 目录中。

- 在`/usr/local/solr-7.7.1/server/solr/mycore/conf/managed-schema`中添加以下内容(就是core对应的配置文件)

  ```bash
  #配置了一个用于index的tokenizer和一个用于query的tokenizer 分词
  #filter 用于过滤不需要的词语  如停用词等等
  
  <fieldType name="text_ik" class="solr.TextField">
      <analyzer type="index">
        <tokenizer class="org.wltea.analyzer.lucene.IKTokenizerFactory" conf="ik.conf" useSmart="false"/>
        <filter class="solr.LowerCaseFilterFactory"/>
      </analyzer>
      <analyzer type="query">
        <tokenizer class="org.wltea.analyzer.lucene.IKTokenizerFactory" conf="ik.conf" useSmart="true"/>
        <filter class="solr.LowerCaseFilterFactory"/>
      </analyzer>
    </fieldType>
  ```

  

- 配置完成以后重启solr服务(当前目录 /usr/local/solr-7.7.1/)

  `bin/solr restart `

- 重启完成以后访问solr服务，按照以下顺序测试ik分词器。

  【图1】

  

- [ ] 参阅

  - [solr7.3 环境搭建 配置中文分词器 ik-analyzer-solr7 详细步骤](https://blog.csdn.net/u011052863/article/details/80281941)

  

----

##### python连接到mysql数据库

- 首先新建数据库和数据表

  ```bash
  #1登录 mysql -u root -p && 输入password
  
  #2新建数据库命名为  data_first
  
  #3新建数据表用于存储数据
  CREATE TABLE IF NOT EXISTS `xls_item`(
     `id` INT UNSIGNED AUTO_INCREMENT,
     `checkitem` VARCHAR(350) NOT NULL,
     PRIMARY KEY ( `id` )
  )ENGINE=InnoDB DEFAULT CHARSET=utf8;
  ```

  

  

- 打开服务器远程端口，可以远程连接数据库。

  - 首先编辑MySQL配置文件，将其中的bind-address = 127.0.0.1注释

    ```bash
    #打开配置文件
    sudo vim /etc/mysql/mysql.conf.d/mysqld.cnf  
    
    #注释bind-address = 127.0.0.1
    ```

    

  - 授权一个叫root的账户，并授予它远程连接的权力

    ```bash
    GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY 'root' WITH GRANT OPTION;
    FLUSH PRIVILEGES;
    ```

    

- 验证代码



-----

##### solr连接数据库并导入数据使用ik分词器建立索引

- solr 配置导入环境(当前工作目录`/usr/local/solr-7.7.1/server/solr/mycore/conf`)

  - 首先安装jar驱动包

    1.  首先下载mysql驱动包 ，大部分jar数据包在[maven](https://mvnrepository.com/)仓库都能找到，mysql驱动包在maven仓库中的下载链接是：[MySQLjar包](http://central.maven.org/maven2/mysql/mysql-connector-java/)
    2. 将 mysql 驱动包导入solr ：将下载下来的 mysql-connector-java-x.x.x.jar 拷贝到 `/usr/local/solr-7.7.1/server/solr-webapp/webapp/WEB-INF/lib `下；
    3. 将`/usr/local/solr-7.7.1/dist`目录下的：`solr-dataimporthandler-7.x.x.jar`和`solr-dataimporthandler-extras-7.x.x.jar`这两个jar包拷贝到`/usr/local/solr-7.7.1/server/solr-webapp/webapp/WEB-INF/lib`下

    

  - 配置`solrconfig.xml`,添加以下内容，并保存退出。

    ```bash
    #<str> 标签中存放的是数据库配置信息的文件名
    
    <requestHandler name="/dataimport" class="solr.DataImportHandler">
        <lst name="defaults">
          <str name="config">data-config.xml</str>
        </lst>
    </requestHandler>
    ```

    

  - 在` data-config.xml`文件中写入如下内容，填写数据库的信息。

    ```bash
    #url中包括ip、端口号、需要连接的数据库
    #填写数据库的用户名和密码
    #entity的name填写数据库中待导入的表名
    
           <!-- 配置数据源 -->
            <!-- url中最后要加上serverTimezone=UTC否则发送请求的时候会乱码 -->
            <dataSource driver="com.mysql.jdbc.Driver"
                                    url="jdbc:mysql://localhost:3306/data_first?serverTimezone=UTC"
                                    user="root"
                                    password="123456"/>
    
    
            <document>
                    <!-- query中写SQL语句 -->
                    <entity name="xls_item" query="select * from xls_item">
                            <!-- column对应数据库中的列名，name为对应的域名（在scheme中没有的话需要配置，即设置业务系统域）,
                            这是一个映射关系 -->
                            <field column="id" name="id"/>
                            <field column="checkitem" name="checkitem"/>
                      </entity>
    
            </document>
    
    </dataConfig>
    ```

  - 然后在`/usr/local/solr-7.7.1/server/solr/mycore/conf/managed-schema`中配置对应的field字段。

    ```bash
    #其中设置的text_ik就是新添加的ik分词器的类型  这样该字段才会被ik分词器解析
    
    <field name="checkitem" type="text_ik" indexed="true" stored="true"/>
    ```

    

  - 配置完成在solr中进行数据库的导入

    【图2】

  - 访问solr进行测试

    

- [ ] 参阅

  - [solr学习篇（三） solr7.4 连接MySQL数据库](https://www.cnblogs.com/yanfeiLiu/p/9272644.html)

  - 如果想系统的了解一下solr的使用方法，建议阅读一下[solr官方手册](https://lucene.apache.org/solr/guide/7_7/about-this-guide.html)

  - [Solr练习1：索引Techproducts示例数据](https://www.w3cschool.cn/solr_doc/solr_doc-2gbo2fsg.html)

  - [A working Java 8 is required to run Solr](https://stackoverflow.com/questions/37124359/a-working-java-8-is-required-to-run-solr)

    



----

##### python编程导入xlsx数据到数据库中

- 首先读取文件中所有的列存储在 [columns.txt](https://github.com/jackcily/16dachuang/blob/solr/xhl/columns.txt)中

- 然后连接数据库 [connect_database.py](https://github.com/jackcily/16dachuang/blob/solr/xhl/connect_databse.py)

- 然后读取xlsx文件，存入数据库中[read_csv.py](https://github.com/jackcily/16dachuang/blob/solr/xhl/read_csv.py)

  

