import datetime
import re


def validated_city(text, data):
    if type(text) is str and re.match('^[a-zA-Z0-9_]+$', text):
        if not text.istitle():
            text = text.capitalize()
        return text


def validated_count_hotel(text, data):
    if text.isdigit():
        c = int(text)
        if 0 < c <= 25:
            return c


def validated_count_people(text, data):
    if text.isdigit():
        c = int(text)
        if 0 < c < 50:
            return c


def validated_price_range(text, data):
    parts = text.split('-')
    if len(parts) == 2:
        if parts[0].isdigit() and parts[1].isdigit():
            start = int(parts[0])
            end = int(parts[1])
            if 0 <= start <= end <= 10000:
                return start, end


def validated_dist_range(text, data):
    parts = text.split('-')
    if len(parts) == 2:
        if parts[0].isdigit() and parts[1].isdigit():
            start = int(parts[0])
            end = int(parts[1])
            if 0 <= start <= end <= 500:
                return start, end


def validated_show_photos(text, data):
    if text in ('Да', 'да'):
        return True
    elif text in ('Нет', 'нет'):
        return False


def validated_count_photos(text, data):
    if text.isdigit():
        c = int(text)
        if 0 < c <= 15:
            return c


def validated_start_year(text, data):
    if text.isdigit():
        year = int(text)
        if datetime.datetime.today().year.real <= year <= 2032:
            return year


def validated_start_month(text, data):
    regex = re.compile('^(0?[1-9]|1[012])$')
    match = regex.match(text)
    if match is not None:
        return int(text)


def validated_start_day(text, data):
    regex = re.compile('^(0?[1-9]|(1|2|3)[0-9])$')
    match = regex.match(text)
    if match is not None:
        day = int(text)
        if data['start_booking_month'] in (1, 3, 5, 7, 8, 10, 12) and day <= 31:
            return day
        elif data['start_booking_month'] == 2 and day <= 28 or data['start_booking_year'] % 4 == 0 and day <= 29:
            return day
        elif day <= 30:
            return day


def validated_end_year(text, data):
    if text.isdigit():
        year = int(text)
        if data['start_booking_year'] <= year <= 2032:
            return year


def validated_end_month(text, data):
    regex = re.compile('^(0?[1-9]|1[012])$')
    match = regex.match(text)
    if match is not None:
        if data['end_booking_year'] < data['start_booking_year'] or int(text) >= data['start_booking_month']:
            return int(text)


def validated_end_day(text, data):
    regex = re.compile('^(0?[1-9]|(1|2|3)[0-9])$')
    match = regex.match(text)
    same = data['end_booking_year'] == data['start_booking_year'] and data['end_booking_month'] == data[
        'start_booking_month']
    bef = data['end_booking_year'] > data['start_booking_year'] or data['end_booking_month'] > data[
        'start_booking_month']
    if match is not None:
        day = int(text)
        if bef or same and day > data['start_booking_day']:
            if data['end_booking_month'] in (1, 3, 5, 7, 8, 10, 12) and day <= 31:
                return day
            elif data['end_booking_month'] == 2 and day <= 28 or data['end_booking_year'] % 4 == 0 and day <= 29:
                return day
            elif day <= 30:
                return day
