import time
import scrapy
from scrapy import Selector
from selenium import webdriver
from selenium.webdriver.common.by import By

from .helper import parse_li


class GzhgzSpider(scrapy.Spider):
    name = "gzhgz"
    allowed_domains = ["www.gzhgz.com"]
    start_urls = ["https://www.gzhgz.com/e/action/ListInfo.php?classid=3857,3862,3866,3870,3878,3874,3886,3890,3882,4063,4018,4014&forajax=1&page=" + str(i) for i in range(0, 100)]

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
            print(each_li)
            print(job)
            yield job

    def closed(self, reason):
        print('fini')
        self.driver.close()



