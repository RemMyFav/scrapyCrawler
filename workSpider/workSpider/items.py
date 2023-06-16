# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
from collections import defaultdict

import scrapy


class JobItem(scrapy.Item):
    工作名称 = scrapy.Field()  # 招聘计划
    招聘计划 = scrapy.Field()  # 招聘计划：人数
    报名时间 = scrapy.Field()  # 报名时间
    招聘地区 = scrapy.Field()  # 招聘地区
    劳动关系 = scrapy.Field()  # 劳动关系
    报名方式 = scrapy.Field()  # 报名方式
    # jobHref = scrapy.Field()  # 网址
    # jobOther = defaultdict(scrapy.Field())  # 其他

