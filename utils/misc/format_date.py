from datetime import datetime


def datetime_to_str(date: datetime) -> str:
    """
    2022-11-05 18:29:26
    :param date:
    :return:
    """
    return f'{date.year.real}-{date.month.real}-{date.day.real} ' \
           f'{date.hour.real}:{date.minute.real}:{date.second.real}'
