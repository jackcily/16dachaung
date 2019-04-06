## 读取xls文件

writen by : cloud0606

## 环境

python3.6

## 思路

应用情景：拿到的数据文件夹下有6534个文件，包含xls文件和xlsx格式的文件，需要读取后按行存入数据库

解决方法：使用pyexcel_xls读取文件，由于每张表的结构不同，包含列的列名和个数都不一样，所以就不打算在数据库中建相似的表，而是把每条数据与列名一起存入数据库。

![20190406-一条数据](D:\大创文件\img\20190406-一条数据.png)

```bash
**例子
# 对于上图的一条数据处理成以下格式存储
# 列名字典
1:序号
2:标称生产企业名称
3:标称生产企业地址
...
12:备注

# 存储的数据
"1:1 2:安庆市正泰老爷爷食品有限公司 3:安徽省安庆市迎宾路山城大厦906室 ..."

```

## 代码

```python
from pyexcel_xls import get_data  # 读取xls文件
import os.path  # 用于读取文件夹下文件名
from mysql import * # xhl写好的连接数据库的函数
def readFileName(folder):
    '读取文件夹下的所有文xls件名'
    filename_list = []
    count_file_all = 0
    list = os.listdir(folder)  # 列出文件夹下所有的目录与文件
    for i in range(0, len(list)):
        filepath = os.path.join(folder, list[i])  # 拼接文件路径
        filename, type = os.path.splitext(filepath)  # 返回 gov_1450299787244 和.xls
        if os.path.isfile(filepath) and type == '.xls': # 只读取xls文件
            count_file_all = count_file_all + 1  # 统计文件数
            filename_list.append(filepath)
            #print(count_file_all, filepath)
    return filename_list

def readXls(filename,dict):
    '读取xls文件 将一行数据转换为一个字符串'
    col_name_num = []
    sql_list = []
    row_count = 0 # 记录文件读取到哪一行
    try:
        data = get_data(filename)  # 读取文件
    except Exception as e:
                print(e)
    else:
        for key in data.keys():
            table = data[key]# 获得对应的表
            # 获取列名添加到字典中
            try:
                for line in table :
                    if '序号' in line:
                        col_name = line
                        for cname in col_name:
                            # 去除列名中不需要的字符\ufeff
                            new_cname = rmov(cname).encode('utf-8').decode('utf-8-sig')
                            if new_cname in dict.keys():
                                col_name_num.append(dict[new_cname])
                            else:
                                print('该列名不在字典中',new_cname)
                        #print('列名------',col_name)
                        #print('序号------', col_name_num)
                        break
                    row_count = row_count + 1
            except Exception as e:
                print('*没有找到属性列*')        
                print(col_name)
            else:
                for line in table[row_count + 1:]:
                    sql = ''
                    for i in range(min(len(col_name_num),len(line))):
                        item = line[i] #取出一个属性值
                        # 如果属性值非空，拼接到查询语句中
                        if item is not None and not (str(item).strip() == ""):  
                            sql = sql + " " + str(col_name_num[i]) + ":" + str(item)
                    sql = sql[:300] #截断一下避免有超长的空字符串
                    if sql != '':
                        sql_list.append(sql)
    return sql_list

def rmov(strings):
    '字符串过滤'
    st = strings.replace("\n","")
    st = st.replace(r"\ufeff","")
    return st

count_item = 0
def createColName(colNameFile):
    '建立关于列名的字典 比如 1:生产标识 '
    col_dict = {}
    index = 1
    with open(colNameFile, 'rt', encoding='utf-8-sig') as f:
        for line in f:
            col_dict.setdefault(rmov(line).encode('utf-8').decode('utf-8-sig'), index)
            index = index + 1
    print("字典中的列名数目:",index)
    return col_dict


if __name__ == "__main__":
    # 创建字典
    dict = createColName('re.txt') #
    # 读取文件内所有文件名
    filename = readFileName("download/")
    # 连接数据库  准备进行数据插入
    conn = connDatabase()
    cur = getcursor(conn)  # 连接数据库
    count = 0 #用于计算一共插入了多少数据
    # 遍历文件插入数据
    for name in filename:
        #print(name)
        sql_data = readXls(name,dict)
        count = count + len(sql_data)
        #print('*****',sql_data)
        #print('【',count,'】')
        for sql in sql_data:
            if len(sql) > 0:
                sql_final = "insert into xls_item(checkitem) values ('" + sql + "');"
                print(sql_final)
                opt(conn, cur, sql_final) # 插入一条数据
    # 关闭数据库
    closeDatabase(conn, cur)  

```
## 遇到的问题

- 读取列名时字符串中出现\ufeff，于是在打开文件时加上`open(colNameFile, 'rt', encoding='utf-8-sig')`就可以，还有部分字符用此方法不管用采用这种方式即可 `new_cname = cname.encode('utf-8').decode('utf-8-sig')`

