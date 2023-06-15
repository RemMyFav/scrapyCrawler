# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
from collections import defaultdict

import scrapy


class JobItem(scrapy.Item):
    jobTitle = scrapy.Field()  # 招聘计划
    jobPlan = scrapy.Field()  # 招聘计划：人数
    jobDate = scrapy.Field()  # 报名时间
    jobLocation = scrapy.Field()  # 招聘地区
    jobType = scrapy.Field()  # 劳动关系
    jobWay = scrapy.Field()  # 报名方式
    jobHref = scrapy.Field()  # 网址
    # jobOther = defaultdict(scrapy.Field())  # 其他

