import requests

from local_config import API_TOKEN
from datetime import date
from typing import Any, Dict, List


BASE_API_URL = 'https://api.clockify.me/api/v1'
REPORTS_API_URL = (
    'https://reports.api.clockify.me/v1/workspaces/640b40037c1c67026f7f0bdd/'
    'reports/summary')
HEADERS = {
    'x-api-key': API_TOKEN,
}


def get_data_from_api(
        first_day: date, last_day: date) -> Dict[str, List[Dict]]:
    try:
        user_id = _get_user_id()
        request_body = _get_request_body(first_day, last_day, user_id)
        report_response = requests.post(
            REPORTS_API_URL, json=request_body, headers=HEADERS)
        data = report_response.json()
        return data
    except Exception as e:
        raise RuntimeError(f'Failed to get data from Clickify API: {e}')


def _get_user_id() -> str:
    user_info_response = requests.get(f'{BASE_API_URL}/user', headers=HEADERS)
    user_info_response.raise_for_status()
    return user_info_response.json()['id']


def _get_request_body(
        first_day: date, last_day: date, user_id: str) -> Dict[str, Any]:
    body = {
        'dateRangeStart': f'{first_day}T00:00:00.000Z',
        'dateRangeEnd': f'{last_day}T23:59:59.999Z',
        'sortOrder': 'ASCENDING',
        'rounding': False,
        'amountShown': 'HIDE_AMOUNT',
        'zoomLevel': 'MONTH',
        'users': {'ids': [user_id]},
        'summaryFilter': {
            'sortColumn': 'GROUP',
            'groups': ['DATE', 'TIMEENTRY'],
            'summaryChartType': 'BILLABILITY',
        }
    }
    return body
