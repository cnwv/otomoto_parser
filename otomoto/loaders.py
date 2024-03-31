from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from datetime import datetime
from urllib.parse import urljoin


def create_text(item):
    result = "".join(item)
    try:
        result.replace('\xa0', '')
    except ValueError:
        result = None
    return result


def get_description(item):
    cleaned_text = "".join(item)
    return cleaned_text


def get_id(item):
    return int(item.pop())


def create_company_url(item):
    return urljoin("https://hh.ru/", item.pop())


def get_formated_price(item):
    time = datetime.now().isoformat()
    price = int(item[0].replace(' ', ''))
    return {'prices': [{'time': time, 'price': price}]}


def get_int(item):
    return int(item[0])


def set_gear_box(item):
    if item[0] == 'Automatyczna':
        return 'automatic'
    elif item[0] == 'Manualna':
        return 'manual'
    else:
        return 'unknown'


def get_km(item):
    return int(item[0].replace(' km', '').replace(' ', ''))


class PassatLoader(ItemLoader):
    default_item_class = dict
    url_out = TakeFirst()
    id_out = get_id
    title_out = TakeFirst()
    price_out = get_formated_price
    year_out = get_int
    car_mileage_out = get_km
    version_out = TakeFirst()
    generation_out = TakeFirst()
    gear_box_out = set_gear_box
    all_attributes_out = TakeFirst()
