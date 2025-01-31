import re
import requests

from datetime import date
from io import StringIO
from lxml import etree
from time import sleep


CONVERTER_URL = 'https://exchangerates.org/{}-eur-to-usd'
RETRY_TIMES = 10


def convert_to_usd(euro_price: str, last_day: date) -> str:
    today = date.today()
    if today < last_day:
        last_day = today
    try:
        euro_price = euro_price.replace('.', '').replace(',', '.')
        response = _get_response_with_converted_price(euro_price)
        usd_price = _parse_response(response, last_day)
        return f'{usd_price:.2f}'
    except Exception as e:
        raise RuntimeError(f'Failed to convert {euro_price} EUR to USD: {e}')


def _get_response_with_converted_price(
        euro_price: str) -> str:
    for retry_time in reversed(range(RETRY_TIMES)):
        response = requests.get(CONVERTER_URL.format(euro_price))
        if response.status_code == 200:
            return response.text
        print(f'Failed to convert, retry time {retry_time}')
        sleep(3)
    else:
        raise RuntimeError('Failed to retrieve data from exchange site')


def _parse_response(response: str, last_day: date) -> float:
    formatted_last_day = last_day.strftime("%d/%m/%Y")
    parser = etree.HTMLParser(recover=True)
    html = etree.parse(StringIO(response), parser)
    raw_price = html.xpath(
        f'//td[contains(., "{formatted_last_day}")]'
        '/following-sibling::td/text()')
    usd_price = re.findall(r'\b(\d+\.\d+)\sUSD', raw_price[0])[0]
    return float(usd_price)
