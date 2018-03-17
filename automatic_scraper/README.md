###  一、安装项目依赖包

```
pip insatll -r requirements.txt
```
### 二、安装浏览器驱动和插件
#### 1. 下载
从 https://gitee.com/xNathan/automatic_scraper/attach_files 下载插件和驱动。
#### 2. 驱动安装
geckodriver为火狐浏览器驱动，chromedriver为chrome浏览器驱动，下载解压后放在项目根目录中。
#### 3. firefox 插件安装
下载解压`firefox 插件.zip`后，将解压后的两个文件拖到火狐浏览器中安装。

### 三、配置项目爬虫
#### 1. 创建自己的目录
在/automatic_scraper/config/bid/目录下创建以自己姓名拼音命名的文件夹，并在新建的目录下创建空文件`__init__.py`。
#### 2. 编写爬虫
1. 新建一个以`省_市_类型_config.py`(常规爬虫)或`省_市_类型_config_fre`(实时爬虫)规则命名的python文件。
若为实时爬虫，需在根目录下的文件`default_config.py`中配置启动时间隔，在`task_config`中添加键值。
key为爬虫文件名，value单位为秒。例如，
```
task_config = {
    "country_zfcg_config_fre":60,
}
```

2. 将模板内容拷贝到自己的爬虫文件。

3. 修改模板


```
author = "Denglixi" # 自己的姓名

web_title = u"池州公共资源交易平台"  # 网站名

data_source = 'http://www.czztbj.cn' # 网站url


start_urls = [
    "http://www.czztbj.cn/chiztpfront/jyxx/002001/002001001/",
    "http://www.czztbj.cn/chiztpfront/jyxx/002002/002002001/",
]  # 填入各栏目列表页的起始链接
```



```
db_config = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': '123456',
    'database': 'bid_data',
    'table': 'zhaotoubiao'
} 
# 配置自己的开发据库
```


```
# 列表页模板
""" 
_list[pattern] 中为列表标签的路径
_list[type] 为pattern的类型，可选xpath或者css
_list[target] 为获取类型，可选html(获取标签)或者text(获取文本)
_next_page 为翻页标签
"""
index_pattern = {
    "_list": {'pattern': "//div[@style='width:980px; margin:10px;']//tr[@height='30']", 'type': 'xpath',
              'target': 'html', 'custom_func_name': ''},
    "_next_page": {'pattern': u"//td[text() = '下页 > and @onclick']", 'type': 'xpath', 'target': 'html',
                   'custom_func_name': ''},
    "issue_time": {'pattern': "//td[@width='80']", 'type': 'xpath', 'target': 'text', 'custom_func_name': ''},
    "title": {'pattern': "//a/@title", 'type': 'xpath', 'target': 'text', 'custom_func_name': ''},
}
```


```
# 详情页模板
"""
获取详情页的信息，使用方法同列表页模板
target 中的clean_html为获取清洗后的html标签，一般不需要更改
"""
detail_pattern = {
    "sc": {'pattern': "//table[@id='tblInfo']",
           'type': 'xpath', 'target': 'clean_html', 'custom_func_name': ''},
}
```

```
def init(item):
    """初始化时执行"""
    logger.info(u'init item: %s', item)
    item['_web_title'] = item['web_title']
    del item['web_title']
    # 设置翻页延迟, 单位为秒
    item['_delay_between_pages'] = 1
```

```
def process_list_item(list_element, item):
    """处理列表页元素
    :param list_element: _list模板解析出的html元素
    :param item:

    获取列表页后，根据_list模板获取每一个详情html代码后执行
    有些内容可在列表页获取，可自定义在此处理，如：
    item['pub_date'] = pq(list_element).find('span').text()
    """
```


```
def process_detail_item(item):
    """处理详情页
    :param item:

    获取详情页信息，存入item后执行
    可在此处理程序无法处理的情况

    如详情页无法解析发布时间，需要使用正则表达式从content中提取等
    """
```

### 四、规范
#### 1. 文件名规范

以`省_市_类型_config.py` 命名爬虫文件为常规爬虫，如`anhui_chizhou_ggzy_config.py`, 
以`省_市_类型_config_fre` 命名爬虫文件为实时爬虫，如`country_zfcg_config_fre.py`, 


若文件名不以`config.py`或`_config_fre.py`为结尾，则该爬虫将无法启动。 

#### 2. 编码规范

1. author 必须与文件夹名一致, 不要使用中文。

2. 注意其他地方使用**中文**时，注意在**引号前加u**，例如
	```
	u'中国'
	u"//div[@id='laypage_0']//a[text()='下一页']"
	```
3. 获取列表页的标签时，获取的是每一条信息的标签，而不是获取整块信息的标签。

4. index_pattern, detail_pattern 中没有下划线的key可存入数据库中，加下划线的key在进入数据前会被删除。

5. 有的网站由于浏览器翻页过慢，导致列表页未完成加载而引起异常抛出，可在`def init()`中的item`['_delay_between_pages']`设置翻页延迟，单位为秒。