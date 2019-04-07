# -*- coding: utf-8 -*-

#目的  读取文件中的csv的文件 拼接成对应的字符串

#首先读取文本文件  新建字典

#然后新建拼接函数   输入字典 和 文件路径  自动生成插入的sql语句

#最后新建数据库函数  给定sql语句 curser 进行数据插入
import os
import xlrd
import pymysql


dict_path="D:/Administrator/desktop_bak/Desktop/re.txt"
folder_path= "D:/Administrator/desktop_bak/Desktop/download/"
maxs=0
cont=""
sum =0
sumrow=0
def rmov(strings):
	st = strings.replace("\n","")
	st = st.replace(r"\ufeff","")
	return st

def connDatabase():  #返回一个连接了数据库的句柄
	conn = pymysql.connect(host='62.234.117.231', port=3306, user='root', password='123456', db='data_first',charset='utf8')
	return conn

def getcursor(conn): #给定已经连接的数据库句柄  获取数据库的操作游标
	cur = conn.cursor()
	return cur

def opt(conn,cur,sql): #给定数据库句柄、数据库的操作游标  进行数据库语句的执行
	try:
		cur.execute(sql)  #执行插入操作
		conn.commit()     #将改变提交到数据库中

	except Exception:
		conn.rollback()   #如果发生异常就进行数据库回滚

def closeDatabase(conn,cur):
	cur.close()
	conn.close()


def buildDict(dict_path):              #输入路径  返回新建完成的字典
	dict_col={}
	index=1
	with open(dict_path, 'rt',encoding='utf-8-sig') as f:
		for line in f:
			dict_col.setdefault(rmov(line),index)
			index=index+1
	#dict_col.setdefault("标示生产企业名称", 1)
	print(len(dict_col))
	f.close()
	return dict_col


def openfile(path):   #输入文件夹路径 返回所有合格xlsx文件的list
	list_xlsx=[]
	list = os.listdir(path)
	index = 0
	for i in list:
		filepath = os.path.join(path, i)   #获得文件路径
		filename, type = os.path.splitext(filepath)
		if os.path.isfile(filepath) and type == '.xlsx':  #判断文件类型 是否是xlsx
			list_xlsx.append(filepath)
	return list_xlsx


def made_sql(fila_name,dicts):   #输入文件名 返回文件的列数

	try:
		data = xlrd.open_workbook(fila_name)
		table = data.sheet_by_index(0)# 获取第一个工作表
		nrows = table.nrows# 获取行数
		ncols = table.ncols# 获取列数
		lie_num=[]  #列名对应的符号
		next=1      #记录列名的后一行
		for i in range(1,nrows):
			excel_rows=[]
			for j in range(ncols):
				cell_value = table.cell(i, j).value # 把数据追加到excel_rows中
				excel_rows.append(cell_value)
			if "序号" in excel_rows:
				next=i+1
				for k in excel_rows:
					lie_num.append(dicts[k])
				break

		for i in range(next,nrows):
			excel_rows=[]
			sql=""
			for j in range(ncols):
				cell_value = table.cell(i, j).value  # 把数据追加到excel_rows中
				excel_rows.append(cell_value)
				if cell_value is not None and not (str(cell_value).strip() ==""):    #如果字符串不是空的
					sql=sql+" "+str(lie_num[j])+":"+str(cell_value)
			#print(sql)

			sql = sql[:300]   #防止字符串过长  进行截断操作

			#如果sql语句不是空的   我就把它插入进去  多余的长度直接进行截断
			#opt(conn, cur, sql)  # 进行数据库的插入操作
			#sql2 = "insert into items(manufacturer_name) values ('haha');"
			if len(sql)>0:
				sql_final = "insert into xls_item(checkitem) values ('" +sql +"');"
				print(sql_final)
				opt(conn, cur, sql_final)




	except Exception:
		print(fila_name+"工作簿打不开")




dict_col = buildDict(dict_path)                          #打开txt文件  新建字典
dict_list=sorted(dict_col.items(),key=lambda x:x[1])
for i in dict_list:
	print(i[0])

list_xlsx = openfile(folder_path)                        #获取文件中所有xlsx文件的路径

#连接数据库  准备进行数据插入
conn = connDatabase()
cur = getcursor(conn)   #连接数据库

for i in list_xlsx:
	made_sql(i,dict_col)

closeDatabase(conn,cur) #关闭数据库

#算出来的平均值有159   那我设置为 300  再多一点 字符串中设置为350
