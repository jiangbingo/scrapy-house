app_secret TxRmSs7AxQlBlMyVkXiV4VoEeEfHtPhRh0rFq4J6j5hE7uRt0000000000000000
license  k8lJdVkD9f1WmIj0vSp8BeK6mXyVyZbGc0eUtF9CdJuCaRtYfAsFqBjJfAq8YwZf
token 7gLdKx8nUnLn1Q2sUiSwAl5KxZ6Ys2iK

scrapy crawl dmoz -s JOBDIR=tutorial/dmoz -o data.json
scrapy crawl img -s JOBDIR=tutorial/img

name = scrapy.Field()           //楼盘名称
location = scrapy.Field()       //楼盘位置
url = scrapy.Field()            //原网址
wylb = scrapy.Field()           //物业类别
xmts = scrapy.Field()           //项目特色
jzlb = scrapy.Field()           //建筑类别
zxzk = scrapy.Field()           //装修状况
hxwz = scrapy.Field()           //环线位置
zxal = scrapy.Field()           //装修案例
rjl = scrapy.Field()            //容积率
lhl = scrapy.Field()            //绿化率
kpsj = scrapy.Field()           //开盘时间
jfsj = scrapy.Field()           //交房时间
wyf = scrapy.Field()            //物业费
wygs = scrapy.Field()           //物业公司
kfs = scrapy.Field()            //开发商
ysxkz = scrapy.Field()          //预售许可证
sldz = scrapy.Field()           //售楼地址
wydz = scrapy.Field()           //物业地址
jtzk = scrapy.Field()           //交通状况
fj = scrapy.Field()             //房价
zdmj = scrapy.Field()           //占地面积
jzmj = scrapy.Field()           //建筑面积
kgsj = scrapy.Field()           //开工时间
jgsj = scrapy.Field()           //竣工时间
cqnx = scrapy.Field()           //产权年限
type_name                       //类型名称
city                            //城市名称
url                             //原网址