from dataclasses import dataclass
from datetime import date
from typing import Dict, List, Union

from local_config import HOURLY_RATE, VACATION_TEXT
from utils import format_number


@dataclass
class RawJob:
    description: str
    date: str
    duration: int


@dataclass
class Job:
    description: str
    date: str
    hours: str
    price: str


@dataclass
class Total:
    hours: str
    price: str


@dataclass
class StructData:
    jobs: List[Job]
    total: Total


def get_struct_data(
            api_data: Dict[str, List[Dict]],
            is_group: bool,
            vacation: Union[None, List[date]],
            extra_jobs: Union[None, List[RawJob]],
        ) -> StructData:
    jobs = _get_jobs(api_data, is_group, vacation, extra_jobs)
    return StructData(
        jobs=_format_jobs(jobs),
        total=_get_total(jobs),
    )


def _get_jobs(
            api_data: Dict[str, List[Dict]],
            is_group: bool,
            vacation: Union[None, List[date]],
            extra_jobs: Union[None, List[RawJob]],
        ) -> List[RawJob]:
    jobs = list()
    grouped_jobs = dict()
    for group in api_data['groupOne']:
        for child in group['children']:
            date_ = child['_id']['DATE']
            description = child['name']
            duration = child['duration']
            jobs.append(_create_raw_job(
                date_, description, duration, is_group, grouped_jobs))
    if not is_group:
        jobs = [RawJob(
            description=key, **value) for key, value in grouped_jobs.items()]
    jobs = _handle_vacation_and_extras(jobs, is_group, vacation, extra_jobs)
    return sorted(jobs, key=lambda job: job.date)


def _create_raw_job(
            date_: str,
            description: str,
            duration: int,
            is_group: bool,
            grouped_jobs: dict
        ) -> Union[RawJob, None]:
    if is_group:
        return RawJob(date=date_, description=description, duration=duration)
    else:
        if description not in grouped_jobs:
            grouped_jobs[description] = {'date': date_, 'duration': duration}
        else:
            grouped_jobs[description]['duration'] += duration
    return None


def _handle_vacation_and_extras(
            jobs: List[RawJob],
            is_group: bool,
            vacation: Union[None, List[date]],
            extra_jobs: Union[None, List[RawJob]],
        ) -> List[RawJob]:
    if vacation:
        if is_group:
            for date_ in vacation:
                jobs.append(RawJob(
                    date=date_.strftime('%Y-%m-%d'),
                    description=VACATION_TEXT,
                    duration=28800,
                ))
        else:
            jobs.append(RawJob(
                date=min(vacation).strftime('%Y-%m-%d'),
                description=VACATION_TEXT,
                duration=28800 * len(vacation),
            ))
    if extra_jobs:
        jobs.extend(extra_jobs)
    return jobs


def _format_jobs(jobs: List[RawJob]) -> List[Job]:
    formatted_jobs = list()
    for job in jobs:
        formatted_job = Job(
            description=job.description,
            date=job.date,
            hours=_seconds_to_hour_min_sec(job.duration),
            price=_calculate_price(job.duration),
        )
        formatted_jobs.append(formatted_job)
    return formatted_jobs


def _get_total(jobs: List[RawJob]) -> Total:
    total_duration = sum([job.duration for job in jobs])
    return Total(
        hours=_seconds_to_hour_min_sec(total_duration),
        price=_calculate_price(total_duration),
    )


def _seconds_to_hour_min_sec(seconds: int) -> str:
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return f'{hours:02d}:{minutes:02d}:{seconds:02d}'


def _calculate_price(seconds: int) -> str:
    hours = seconds / 3600
    price = hours * HOURLY_RATE
    return format_number(round(price, 2))
