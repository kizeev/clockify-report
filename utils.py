import calendar
import os

from argparse import ArgumentParser
from datetime import date
from decimal import Decimal
from typing import Tuple, Dict

from local_config import (
    GROUP_BY_DAYS, CONVERT_TO_USD, ADD_GERMAN_LANGUAGE, ADD_VACATION,
    ADD_EXTRA_EXPENSES_PREMIUMS)


def get_args_from_cmd(
        ) -> Dict[str, Tuple[int, int, bool, bool, bool, bool, bool]]:
    arg_parser = ArgumentParser()
    arg_parser.add_argument('-y', type=int, help='The year like 2023')
    arg_parser.add_argument('-m', type=int, help='The month like 12')
    arg_parser.add_argument(
        '-g', action='store_true', default=GROUP_BY_DAYS,
        help='Group by tasks by days')
    arg_parser.add_argument(
        '-usd', action='store_true', default=CONVERT_TO_USD,
        help='Convert EUR to USD')
    arg_parser.add_argument(
        '-de', action='store_true', default=ADD_GERMAN_LANGUAGE,
        help='Add German language')
    arg_parser.add_argument(
        '-v', action='store_true', default=ADD_VACATION, help='Add vacation')
    arg_parser.add_argument(
        '-e', action='store_true', default=ADD_EXTRA_EXPENSES_PREMIUMS,
        help='Add extra expenses/premiums')
    args = arg_parser.parse_args()

    if args.y and args.m:
        return vars(args)
    else:
        print("Error: Both year (-y) and month (-m) must be specified.")
        exit(1)


def get_days_of_month(year: int, month: int) -> Tuple[date, date]:
    first_day = date(year, month, 1)
    _, number_of_days = calendar.monthrange(year, month)
    last_day = date(year, month, number_of_days)
    return first_day, last_day


def format_number(number: float) -> str:
    return '{:n}'.format(Decimal(f'{number:.2f}'))


def create_output_dir():
    if not os.path.exists('output'):
        os.makedirs('output')
