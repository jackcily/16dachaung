# -*- coding: utf-8 -*-
#没有语法错误但是插入失败

import pymysql

def connDatabase():  #返回一个连接了数据库的句柄
	conn = pymysql.connect(host='xxx.xxx.xxx.xxx', port=3306, user='xxx', password='xxx', db='xxxx',charset='utf8')
	return conn

def getcursor(conn): #给定已经连接的数据库句柄  获取数据库的操作游标
	cur = conn.cursor()
	return cur

def opt(conn,cur,sql): #给定数据库句柄、数据库的操作游标  进行数据库语句的执行
	try:
		cur.execute(sql)  #执行插入操作
		conn.commit()     #将改变提交到数据库中
	except:
		conn.rollback()   #如果发生异常就进行数据库回滚

def closeDatabase(conn,cur):
	cur.close()
	conn.close()

sql = "insert into items(manufacturer_name) values ('haha');"


conn = connDatabase()
cur = getcursor(conn)   #连接数据库
for i in range(0,5):
	opt(conn,cur,sql)   #进行数据库的插入操作
closeDatabase(conn,cur) #关闭数据库