## php处理用户查询

writen by :cloud0606

## 1. 环境

PHP 7.0.33-0ubuntu0.16.04.3 (cli) ( NTS )

php-curl : 1:7.0+35ubuntu6.1

```bash
# 安装
sudo apt-install -y php-curl
systemctl restart apache2 # 一定要重启服务
```

## 2.  思路

- 应用场景：我们的数据都已经导入到了solr中，可以直接通过url的形式到solr中进行搜索，但是由于受到我们存储数据格式的影响，需要对查询结果进行格式处理，所以用php进行衔接

- 数据存储格式

    ```
    属性代号1：属性值1 属性代号2：属性值2 属性代号3：属性值3 属性代号4：属性值4
    ```
    此外还有一个字典存储属性代号对应的属性名

    ```bash
    **例子
    # 列名字典
    属性代号：属性值
    1:编号
    2:企业名称
    3:规格型号
    ...
    
    # 数据库中数据
    "1:1000234 2:三只松鼠股份有限公司  3:225g/袋"
    
    # 对应翻译后的数据信息
    编号:1000234
    企业名称:三只松鼠股份有限公司
    规格型号:225g/袋
    
    ```

- solr 查询结果截图

	![20190406-solr查询结果截图](D:\大创文件\img\20190406-solr查询结果截图.png)

- php完成的功能

  - 获取用户get请求中的参数并使用curl查询solr
  - 查询结果格式化处理

## 3. 代码结构

### 使用curl查询solr

```php
// 获取用户get请求中的keyword
$keyword = $_GET['keyword'];
$url = "http://62.234.117.231:8983/solr/mycore/select?rows=2&q=checkitem:".urlencode($keyword);//有中文所以需要urlencode

// 初始化
$ch = curl_init();
// 设置选项，包括URL
curl_setopt($ch, CURLOPT_URL, $url);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
curl_setopt($ch, CURLOPT_HEADER, 0);
// 执行并获取HTML文档内容
$output = curl_exec($ch);
//释放curl句柄
curl_close($ch);

$output_arr = json_decode($output,true);//查询结果编码为数组
```

### 查询结果处理

首先根据之前筛选出的列名txt文件建立字典，然后把solr查询结果（一大长串字符串）结构化（转为Array）。


```php
// 1.建立列名字典
$file = fopen("/home/ubuntu/re.txt","r");
$arr_col = array();
$i=1;

while(!feof($file))
{
  $tmp =  fgets($file);  //从文件中读取一行
  if($tmp!="")  //如果字符串不为空就进行存储
  {
      $tmp1 = str_replace("\r\n",'',$tmp);//由于在往数据库中插入数据的时候没有去除\r\n,为保持序号的同步性，且不想在输出结果中出现\r\n，所有在字典中存储键值对后再过滤\r\n
      $arr_col[$i] = $tmp1;
      $i++;
  }
}

// 2.查询结果格式化
$data =  $output_arr["response"]["docs"];//solr查询结果是json格式，从中取出数据部分
$item_num = 2;//返回结果的数目

$data_return = array();//存储查询结果的数组

for($i=0;$i<$item_num;++$i)
{
  $item_val = $data[(string)$i]["checkitem"];// checkitem是solr中定义的一个field，
  $item_val_ls = explode(' ',$item_val); // 空格切分字符串
  $item_return = array();// 存储一条查询结果
    
  for($index=0;$index<count($item_val_ls);$index++)
  {
    $key_val = explode(':',$item_val_ls[$index]);//冒号切分键值
    $key = $arr_col[(int)$key_val[0]];//根据字典查询列名序号对应的列名
    $val = $key_val[1];
    if ($key == null or $val == null){
      continue;
    }
    $item_return[$key]=$val;
  }
    
  array_push($data_return,$item_return);
}

print_r($data_return);//直接返回给前端
```

