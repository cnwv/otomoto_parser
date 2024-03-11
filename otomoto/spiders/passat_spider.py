from pathlib import Path
import scrapy
from otomoto.loaders import PassatLoader


class PassatSpider(scrapy.Spider):
    name = "otomoto"
    allowed_domains = ["otomoto.pl"]
    start_urls = ["https://www.otomoto.pl/osobowe/volkswagen/passat/od-2015"]
    _xpath_selectors = {'pagination': '//li[@data-testid="pagination-list-item"]/a/@href',
                        'car': '//article[@data-media-size="small"]/section//h1/a/@href'
                        }

    _xpath_data_selectors = {'id': '//p[text()="ID"][last()]/text()',
                             'title': '//h3[contains(@class, "offer-title")]/text()',
                             'price': '//h3[contains(@class, "offer-price__number")]/text()',
                             'year': '//p[text()="Rok produkcji"]/following-sibling::p/text()',
                             'car_mileage': '//p[text()="Przebieg"]/following-sibling::p/text()',
                             'version': '//p[text()="Wersja"]/following-sibling::a/text()',
                             'generation': '//p[text()="Generacja"]/following-sibling::a/text()',
                             'gear_box': '//p[text()="Skrzynia biegów"]/following-sibling::a/text()',
                             }

    def _get_follow(self, response, selector_str, callback):
        for itm in response.xpath(selector_str):
            yield response.follow(itm, callback=callback)

    def parse(self, response, *args, **kwargs):
        yield from self._get_follow(response, self._xpath_selectors['pagination'], self.parse)
        yield from self._get_follow(response, self._xpath_selectors['car'], self.car_parse)

    def car_parse(self, response):
        print('парсинг тачки')
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
