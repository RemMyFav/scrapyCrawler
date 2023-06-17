import time
import scrapy
from scrapy import Selector
from selenium import webdriver
import urllib.parse
import re
from .helper import parse_li

TARGET = "https://www.gzhgz.com"
PAGING = "https://www.gzhgz.com/e/action/ListInfo.php?classid=3857,3862,3866,3870,3878,3874,3886,3890,3882,4063,4018,4014&forajax=1&page="
FLAG = '<li class="article" data-icon="false">'
class GzhgzSpider(scrapy.Spider):
    name = "gzhgz"
    allowed_domains = ["www.gzhgz.com"]
    # start_urls = ["https://www.gzhgz.com/e/action/ListInfo.php?classid=3857,3862,3866,3870,3878,3874,3886,3890,3882,4063,4018,4014&forajax=1&page=" + str(i) for i in range(0, 100)]
    start_urls = [
        "https://www.gzhgz.com/e/action/ListInfo.php?classid=3857,3862,3866,3870,3878,3874,3886,3890,3882,4063,4018,4014&forajax=1&page=0"]
    i = 170
    def start_requests(self):
        # driver = webdriver.Chrome()  # Instantiate a Chrome web driver
        # for url in self.start_urls:
        #     driver.get(url)  # Navigate to the URL
        #     html_content = driver.page_source  # Get the page source
        #     response = scrapy.http.HtmlResponse(url=url, body=html_content, encoding='utf-8')
        #     yield scrapy.Request(url, self.parse, meta={'driver': driver, 'response': response})
        driver = webdriver.Chrome()
        while True:
            url = PAGING + str(self.i)
            driver.get(url)
            html_content = driver.page_source
            # print(html_content)
            self.i += 1
            if FLAG not in html_content:
                print("flag")
                break
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
            url = scrapy.http.response.urljoin(url=href, base=TARGET)
            job.fields["web"] = scrapy.Field()
            job["web"] = url
            yield scrapy.Request(url, callback=self.parse_sub, meta={'job': job})

    def parse_sub(self, response):
        job = response.meta['job']
        sel = Selector(response=response)
        shell = sel.css('.rsrc_intro').get() or ''
        match_info = re.search('单位名称：(?P<name>[^<]*).+?href="(?P<url>[^"]*)', shell)
        job.fields["company"] = scrapy.Field()
        job.fields["email"] = scrapy.Field()
        job.fields["apply"] = scrapy.Field()
        job.fields["companyWeb"] = scrapy.Field()
        job.fields["video"] = scrapy.Field()
        if match_info:
            name = match_info.group("name")
            url = match_info.group("url").replace("&amp;", "&")
            job["company"] = name
            job["companyWeb"] = url
        match_video = re.search('视频课程：.+?href="(?P<video_url>[^"]*)', shell)
        if match_video:
            video = match_video.group("video_url").replace("&amp;", "&")
            job["video"] = video
        match_mail = re.search('报名邮箱：.+?href="(?P<mail_url>[^"]*)', shell)
        if match_mail:
            mail = match_mail.group("mail_url").replace("&amp;", "&")
            mail = urllib.parse.unquote(mail)
            job["email"] = mail
        match_link = re.search('报名网址：.+?href="(?P<link_url>[^"]*)', shell)
        if match_link:
            link = match_link.group("link_url").replace("&amp;", "&")
            job["apply"] = link
        yield job

    def close(self, reason):
        print("close spider")
        self.crawler.engine.close_spider(self, reason)
