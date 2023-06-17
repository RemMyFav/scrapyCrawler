import re

import scrapy
from scrapy import Selector
from workSpider.items import JobItem

COMMON_ATTRIBUTE = ['招聘计划', '报名方式', '报名时间', '招聘地区', "劳动关系", "笔试时间", "面试时间"]


def parse_li(li):
    """
    <li class="article" data-icon="false"><a data-ajax="false" href="/show-3890-45463.html"><p>
    <strong>都匀泊宁高级中学2023年招聘教师简章</strong></p><p style="white-space: no<br>报名方式：电子邮件<br>
    报名时间：6月14日至8月20日<br>招聘地区：黔南<br>劳动关系：民营企业合同制</p> <p class="ui-li-aside">
    <strong></strong></p></a></li>
    2023-06-14 16:12:26 [scrapy.core.scraper] DEBUG: Scraped from <200 https://www.gzhgz.com/>
    """
    # noinspection PyBroadException
    try:
        # href = re.search('.+?href=\"(?P<url>[^"><p>]*)', li).group("url")
        title = re.search('.+?<strong>(?P<title>[^<]*).+?', li).group("title")
        attrs = re.search('<p style=.+?>(?P<attrs>[^.]*)<p class="ui-li-aside">', li).group("attrs")
        attr = attrs.replace("</p>", "").strip().split("<br>")
        attr_value = {}
        for line in attr:
            line = line.split("：")
            attr_value[line[0]] = line[1]
        # print(attr_value)
        job = JobItem()
        job["name"] = title
        # job["jobHref"] = href
        job["plan"] = attr_value.get("招聘计划") or ''
        job["method"] = attr_value.get("报名方式") or ''
        job["date"] = attr_value.get("报名时间") or ''
        job["location"] = attr_value.get("招聘地区") or ''
        job["relation"] = attr_value.get("劳动关系") or ''
        job["test"] = attr_value.get("笔试时间") or ''
        job["interview"] = attr_value.get("面试时间") or ''
        for key in attr_value.keys():
            if key not in COMMON_ATTRIBUTE:
                job.fields[key] = scrapy.Field()
                job[key] = attr_value.get(key)
                # print(job)
        return job
    except Exception as e:
        print(e)
        return job

# print(parse_li('<li class="article" data-icon="false"><a data-ajax="false" href="/show-3878-41556.html"><p> <strong>毕节市人力资源开发有限责任公司2023年面向社会公开招聘2名劳务派遣员工派遣到毕节市城乡规划技术中心工作公告</strong></p><p style="white-space: normal;">招聘计划：2人<br>报名方式：网络报名<br>报名时间：6月12日至6月14日<br>招聘地区：毕节<br>劳动关系：事业单位劳务派遣</p> <p class="ui-li-aside"> <strong></strong></p></a></li>'))
