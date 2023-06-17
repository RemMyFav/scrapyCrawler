# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
from collections import defaultdict

import scrapy


class JobItem(scrapy.Item):
    name = scrapy.Field()  # 招聘计划
    plan = scrapy.Field()  # 招聘计划：人数
    date = scrapy.Field()  # 报名时间
    location = scrapy.Field()  # 招聘地区
    relation = scrapy.Field()  # 劳动关系
    method = scrapy.Field()  # 报名方式
    test = scrapy.Field()  # 笔试时间
    interview = scrapy.Field()  #面试时间
    # jobHref = scrapy.Field()  # 网址
    # jobOther = defaultdict(scrapy.Field())  # 其他

