import locale

from api import get_data_from_api
from converter import convert_to_usd
from data import get_struct_data
from doc import add_data_to_doc
from input_handler import get_vacation_dates, get_extra_jobs
from local_config import LOCALE
from utils import get_args_from_cmd, get_days_of_month, create_output_dir


def main() -> None:
    locale.setlocale(locale.LC_ALL, LOCALE)
    create_output_dir()

    args = get_args_from_cmd()
    first_day, last_day = get_days_of_month(args['y'], args['m'])
    vacation = get_vacation_dates(first_day, last_day) if args['v'] else None
    extra_jobs = get_extra_jobs(last_day) if args['e'] else None
    api_data = get_data_from_api(first_day, last_day)
    data = get_struct_data(api_data, args['g'], vacation, extra_jobs)
    usd_price = convert_to_usd(
        data.total.price, last_day) if args['usd'] else None
    add_data_to_doc(data, last_day, args['g'], usd_price, args['de'])
    print('Done!')


if __name__ == '__main__':
    main()
