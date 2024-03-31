import scrapy
from otomoto.loaders import PassatLoader
import logging

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())


class PassatSpider(scrapy.Spider):
    name = "otomoto"
    allowed_domains = ["otomoto.pl"]
    start_urls = ["https://www.otomoto.pl/osobowe/volkswagen/passat/od-2015"]
    _xpath_selectors = {'car': '//article[@data-media-size="small"]/section//h1/a/@href'}
    _xpath_data_selectors = {'id': '//p[text()="ID"][last()]/text()',
                             'title': '//h3[contains(@class, "offer-title")]/text()',
                             'price': '//h3[contains(@class, "offer-price__number")]/text()',
                             'year': '//p[text()="Rok produkcji"]/following-sibling::p/text()',
                             'car_mileage': '//p[text()="Przebieg"]/following-sibling::p/text()',
                             'version': '//p[text()="Wersja"]/following-sibling::a/text()',
                             'generation': '//p[text()="Generacja"]/following-sibling::a/text()',
                             'gear_box': '//p[text()="Skrzynia biegów"]/following-sibling::a/text()',
                             }

    def start_requests(self):
        self.logger.info('Start parsing')
        yield scrapy.Request(url=self.start_urls[0], callback=self.parse_page_count)

    def parse_page_count(self, response):
        total_pages = response.xpath('//li[contains(@data-testid, "pagination-list-item")]/a/span/text()')[-1].get()
        for i in range(1, int(total_pages) + 1):
            url = f'{self.start_urls[0]}?page={i}'
            yield response.follow(url, self.parse)

    def _get_follow(self, response, selector_str, callback):
        for itm in response.xpath(selector_str):
            yield response.follow(itm, callback=callback)

    def parse(self, response, *args, **kwargs):
        self.logger.info(f'Parsing page: {response.url} Code: {response.status}')
        yield from self._get_follow(response, self._xpath_selectors['car'], self.car_parse)

    def car_parse(self, response):
        self.logger.info(f'Parsing car: {response.url} Code: {response.status}')
        loader = PassatLoader(response=response)
        loader.add_value('url', response.url)
        for key, xpath in self._xpath_data_selectors.items():
            loader.add_xpath(key, xpath)
        loader.add_value('all_attributes', self.parse_attributes(response))
        yield loader.load_item()

    def parse_attributes(self, response):
        result = {}
        xpath = '///div[@data-testid="advert-details-item"]'
        items = response.xpath(xpath)
        for item in items:
            key = item.xpath('.//p[1]/text()').get()
            value = item.xpath('.//p[2]/text()').get()
            if value is None:
                value = item.xpath('.//a/text()').get()
            result[key] = value
        return result
