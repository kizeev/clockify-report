from datetime import date
from docxtpl import DocxTemplate
from typing import Union

from data import StructData
from local_config import HOURLY_RATE, SENDER_NAME
from utils import format_number


def add_data_to_doc(
            data: StructData,
            last_day: date,
            is_group: bool,
            usd_price: Union[str, None],
            de: bool,
        ) -> None:
    doc = DocxTemplate('template.docx')
    rate = format_number(float(HOURLY_RATE))
    context = {
        'invoice_creation_date': f'{last_day.strftime("%d.%m.%Y")}',
        'invoice_number': f'{last_day.strftime("%m/%Y")}',
        'invoice_period': f'{last_day.strftime("%m.%Y")}',
        'hourly_rate': rate,
        'table_rows': data.jobs,
        'total_hours': data.total.hours,
        'total_price': data.total.price,
        'is_group': is_group,
        'hours_worked': data.total.hours.split(':')[0],
        'minutes_worked': data.total.hours.split(':')[1],
    }

    if usd_price:
        context.update({
            'usd_text': 'Total amount in USD',
            'total_price_usd': f'{format_number(float(usd_price))} USD',
        })

    if de:
        context.update({
            'de_text1': '/ Rechnung',
            'de_text2': 'Programmierung in Python für ',
            'de_text3': rate,
            'de_text4': ' Euro pro Stunde',
            'de_text5': ' / geleistete Stunden',
            'de_text6': ' / Gesamtbetrag netto',
            'de_text7': ' / Rechnungsbetrag',
            'de_text8': (
                '\nBitte überweisen Sie den Rechnungsbetrag auf mein Konto'),
        })

    doc.render(context)
    doc.save(
        f'output/RG_invoice_{SENDER_NAME.replace(" ", "_")}_'
        f'{last_day.strftime("%m_%Y")}.docx')
