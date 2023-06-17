import openpyxl
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class WorkspiderPipeline:
    def __init__(self):
        self.workBook = openpyxl.Workbook()
        self.workSheet = self.workBook.active
        self.workSheet.title = "贵州好工作爬虫列表"
        self.workSheet.append(["工作名称", "单位名称", "页面网址", "劳动关系", "报名时间", "笔试时间", "面试时间",
                                  "招聘地区", "招聘计划", "报名方式", "报名邮箱", "报名网址", "视频课程", "单位网址"])

    def close_spider(self, spider):
        print("show excel")


    def process_item(self, item, spider):
        name = item.get('name') or ''
        company = item.get('company') or ''
        web = item.get('web') or ''
        relation = item.get('relation') or ''
        date = item.get('date') or ''
        test = item.get('test') or ''
        interview = item.get('interview') or ''
        location = item.get('location') or ''
        plan = item.get('plan') or ''
        method = item.get('method') or ''
        email = item.get('email') or ''
        apply = item.get('apply') or ''
        video = item.get('video') or ''
        companyWeb = item.get('companyWeb') or ''
        self.workSheet.append([name, company, web, relation, date, test, interview, location, plan, method, email, apply, video, companyWeb])
        self.workBook.save("5贵州好工作.xlsx")
        return item
