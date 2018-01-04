# 永辉超市全站数据
### 数据总数:843146

数据分级爬取：城市-店铺-种类-商品

##### 网站token
access_token = 'YH601933yCzc'

##### 数据接口
```
#所有城市接口
api_citys = 'https://activity.yonghuivip.com/api/app/shop/citys?'
#城市所有店铺api
api_stores = 'https://activity.yonghuivip.com/api/app/shop/storelist?'
#店铺下所有种类api
api_category = 'https://activity.yonghuivip.com/api/app/v4/search/sellercategory?'
#所有商品api
api_goods = 'https://activity.yonghuivip.com/api/app/v4/search/sellersku?'
```
#### sign签名破解:

sign_str = 'YH601933yCzc'+'传进去的所有参数按照key排序，然后拼接'

