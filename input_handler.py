from datetime import date
from typing import List

from local_config import HOURLY_RATE
from data import RawJob


def get_vacation_dates(first_day: date, last_day: date) -> List[date]:
    while True:
        input_dates = input(
            f'Please give vacation dates [{first_day.day}-{last_day.day}] '
            '(like "9 10 11 12 13 16 17"): ')
        try:
            dates = [
                date(first_day.year, first_day.month, day_number) for
                day_number in map(int, input_dates.split(' '))]
            return dates
        except ValueError:
            print('Error: please enter valid day numbers!')


def get_extra_jobs(last_day: date) -> List[RawJob]:
    extra_jobs = list()
    while True:
        try:
            description = input(
                'Please give description of expenses/premiums: ')
            price = input(
                'Please give price of expenses/premiums (like "125.5"): ')
            extra_jobs.append(RawJob(
                description=description,
                date=last_day.strftime('%Y-%m-%d'),
                duration=int(float(price) / HOURLY_RATE * 3600),
            ))
            any_more = input('Any more? [y/n]: ').lower()
            if any_more != 'y':
                break
        except ValueError:
            print('Error: Please enter a valid price!')
    return extra_jobs
