import datetime
from typing import Callable

from telebot.types import Message

from config_data.config import URL_HOTELS
from config_data.settings import MESSAGES
from hotel.rapid_api import get_city_api
from hotel.get_hotels_data import info_hotels_properties, filter_results_hotels
from loader import bot, history
from states.states import MyStates
from utils.set_bot_commands import set_state_commands, set_hotel_commands


def get_state(key: str):
    if key == 'city':
        return MyStates.city
    if key == 'count_hotels':
        return MyStates.count_hotels
    if key == 'start_booking_year':
        return MyStates.start_booking_year
    if key == 'start_booking_month':
        return MyStates.start_booking_month
    if key == 'start_booking_day':
        return MyStates.start_booking_day
    if key == 'end_booking_year':
        return MyStates.end_booking_year
    if key == 'end_booking_month':
        return MyStates.end_booking_month
    if key == 'end_booking_day':
        return MyStates.end_booking_day
    if key == 'amount_people':
        return MyStates.amount_people
    if key == 'price_range':
        return MyStates.price_range
    if key == 'dist_range':
        return MyStates.dist_range
    if key == 'show_photos':
        return MyStates.show_photos
    if key == 'count_photos':
        return MyStates.count_photos


def change_state(message: Message, key, msg):
    bot.send_message(message.chat.id, msg)
    bot.set_state(message.from_user.id, get_state(key), message.chat.id)


def start(message: Message, command, history_id):
    set_state_commands(bot)
    change_state(message, 'city', MESSAGES['city']['question'])
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['command'] = command
        data['history_id'] = history_id


def validate_data_and_proceed(message: Message, key: str, next_key: str, validate: Callable):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data[key] = validate(message.text, data)

        if data[key] is not None:
            if key == 'city':
                data['city_id'] = get_city_api(data['city'])
                if data['city_id'] is not None:
                    history.update_command(data['history_id'], data['city'])
                else:
                    change_state(message, key, MESSAGES[key]['onservererror'])
                    return

            if key == "show_photos" and data["show_photos"] is False:
                next_key = 'final'
            if next_key == '':
                if data['command'] == "bestdeal":
                    next_key = 'price_range'
                else:
                    next_key = 'show_photos'
            if next_key == 'final':
                result(message, data)
                return
            else:
                change_state(message, next_key, MESSAGES[next_key]['question'])
            return

    change_state(message, key, MESSAGES[key]['onerror'])


def reset(message: Message):
    bot.delete_state(message.from_user.id, message.chat.id)
    set_hotel_commands(bot)


def result(message: Message, data):
    # reset(message)
    bot.send_message(message.chat.id, MESSAGES['final']['question'])

    data['start_date'] = datetime.datetime(year=data['start_booking_year'],
                                           month=data['start_booking_month'],
                                           day=data['start_booking_day']).date()
    data['end_date'] = datetime.datetime(year=data['end_booking_year'],
                                         month=data['end_booking_month'],
                                         day=data['end_booking_day']).date()

    data_properties = info_hotels_properties(data)

    info_hotels_dict = None
    if data_properties is not None:
        info_hotels_dict = filter_results_hotels(data, data_properties)

    if info_hotels_dict is None:
        bot.send_message(message.chat.id, 'Сервер не отвечает.')
        return

    num_hotel = 1
    bot.send_message(message.chat.id, 'Результаты поиска отелей:')
    if type(info_hotels_dict) is not dict:
        if type(info_hotels_dict) is str:
            history.insert_result(data['history_id'], info_hotels_dict)
            bot.send_message(message.chat.id, info_hotels_dict)
        return
    for key, value in info_hotels_dict.items():
        history.insert_result(data['history_id'], key)
        bot.send_message(message.chat.id, '_' * 10 + f' Отель №{str(num_hotel)} ' + '_' * 10)
        bot.send_message(message.chat.id, f'Название отеля: <a href="{URL_HOTELS % value["id"]}"><b>{key}</b></a>',
                         parse_mode="html")
        otvet = ""
        for keyy, vvalue in value.items():
            if type(vvalue) is str:
                if "https:" in vvalue:
                    bot.send_photo(message.chat.id, f'{vvalue}')
                else:
                    otvet = otvet + f'{keyy}: {vvalue}\n'
        bot.send_message(message.chat.id, otvet)
        num_hotel += 1
