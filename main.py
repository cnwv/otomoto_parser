from scrapy.crawler import CrawlerProcess
from otomoto.spiders.passat_spider import PassatSpider
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings


if __name__ == '__main__':
    crawler_setting = get_project_settings()
    configure_logging(crawler_setting)
    crawler_setting.setmodule("otomoto.settings")
    crawler_process = CrawlerProcess(settings=crawler_setting)
    crawler_process.crawl(PassatSpider)
    crawler_process.start()

