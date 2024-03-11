from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from otomoto.spiders.passat_spider import PassatSpider

if __name__ == '__main__':
    crawler_setting = Settings()
    crawler_setting.setmodule("otomoto.settings")
    crawler_process = CrawlerProcess(settings=crawler_setting)
    crawler_process.crawl(PassatSpider)
    crawler_process.start()
