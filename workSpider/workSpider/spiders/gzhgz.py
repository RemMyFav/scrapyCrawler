import time
import scrapy
from scrapy import Selector
from selenium import webdriver
import urllib.parse
import re
from .helper import parse_li

TARGET = "https://www.gzhgz.com"


class GzhgzSpider(scrapy.Spider):
    name = "gzhgz"
    allowed_domains = ["www.gzhgz.com"]
    # start_urls = ["https://www.gzhgz.com/e/action/ListInfo.php?classid=3857,3862,3866,3870,3878,3874,3886,3890,3882,4063,4018,4014&forajax=1&page=" + str(i) for i in range(0, 100)]
    start_urls = [
        "https://www.gzhgz.com/e/action/ListInfo.php?classid=3857,3862,3866,3870,3878,3874,3886,3890,3882,4063,4018,4014&forajax=1&page=0"]

    def start_requests(self):
        driver = webdriver.Chrome()  # Instantiate a Chrome web driver
        for url in self.start_urls:
            driver.get(url)  # Navigate to the URL
            html_content = driver.page_source  # Get the page source
            response = scrapy.http.HtmlResponse(url=url, body=html_content, encoding='utf-8')
            yield scrapy.Request(url, self.parse, meta={'driver': driver, 'response': response})

    def parse(self, response):
        driver = response.meta['driver']
        sel = Selector(response=response.meta['response'])
        all_li = sel.css('.article').getall()
        count = 0
        for each_li in all_li:
            count += 1
            job = parse_li(each_li)
            href = re.search('.+?href=\"(?P<url>[^"><p>]*)', each_li).group("url")
            job.fields["页面网址"] = scrapy.Field()
            job["页面网址"] = href
            url = scrapy.http.response.urljoin(url=href, base=TARGET)
            yield scrapy.Request(url, callback=self.parse_sub, meta={'job': job})
        driver.close()

    def parse_sub(self, response):
        job = response.meta['job']
        sel = Selector(response=response)
        shell = sel.css('.rsrc_intro').get()
        match_info = re.search('单位名称：(?P<name>[^<]*).+?href="(?P<url>[^"]*)', shell)
        job.fields["单位名称"] = scrapy.Field()
        job.fields["报名邮箱"] = scrapy.Field()
        job.fields["报名网址"] = scrapy.Field()
        job.fields["单位网址"] = scrapy.Field()
        job.fields["视频课程"] = scrapy.Field()
        if match_info:
            name = match_info.group("name")
            url = match_info.group("url").replace("&amp;", "&")
            job["单位名称"] = name
            job["单位网址"] = url
        match_video = re.search('视频课程：.+?href="(?P<video_url>[^"]*)', shell)
        if match_video:
            video = match_video.group("video_url").replace("&amp;", "&")
            job["视频课程"] = video
        match_mail = re.search('报名邮箱：.+?href="(?P<mail_url>[^"]*)', shell)
        if match_mail:
            mail = match_mail.group("mail_url").replace("&amp;", "&")
            mail = urllib.parse.unquote(mail)
            job["报名邮箱"] = mail
        match_link = re.search('报名网址：.+?href="(?P<link_url>[^"]*)', shell)
        if match_link:
            link = match_link.group("link_url").replace("&amp;", "&")
            job["报名网址"] = link
        yield job

    # def closed(self, reason):
    #     print('fini')
    #     self.driver.close()
