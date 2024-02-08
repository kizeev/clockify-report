import requests

from datetime import date
from typing import Dict, List, Union


API_URL = 'https://exchangerates.org/ajax/getChart'
HEADERS = {
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'X-Requested-With': 'XMLHttpRequest',
}
BODY = 'base_id=49&tocode=USD&days=30&amount={}'


def convert_to_usd(euro_price: str, last_day: date) -> str:
    try:
        euro_price = euro_price.replace('.', '').replace(',', '.')
        api_data = _get_data_from_api(euro_price)
        usd_price = _parse_api_data(api_data, last_day)
        return f'{usd_price:.2f}'
    except Exception as e:
        raise RuntimeError(f'Failed to convert {euro_price} EUR to USD: {e}')


def _get_data_from_api(euro_price: str) -> Dict[str, List[Union[str, float]]]:
    try:
        response = requests.post(
            API_URL, BODY.format(euro_price), headers=HEADERS)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f'Failed to retrieve data from exchange API: {e}')


def _parse_api_data(
        api_data: Dict[str, List[Union[str, float]]], last_day: date) -> float:
    struct_data = dict(zip(api_data['dates'], api_data['rates']))
    usd_price = struct_data[last_day.strftime("%Y-%m-%d")]
    return float(usd_price)
