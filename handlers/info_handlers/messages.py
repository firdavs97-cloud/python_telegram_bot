from telebot import custom_filters
from telebot.types import Message

from states import user_state
from loader import bot
from states.states import MyStates
from utils.misc import validate


# Any state
@bot.message_handler(state="*", commands=['cancel'])
def any_state(message):
    """
    Cancel state
    """
    user_state.result(message, "Отменена.")


@bot.message_handler(state=MyStates.city)
def bot_get_hotel_count(message: Message):
    user_state.validate_data_and_proceed(message, 'city', 'count_hotels', validate.validated_city)


@bot.message_handler(state=MyStates.count_hotels)
def bot_get_booking_year(message: Message):
    user_state.validate_data_and_proceed(message, 'count_hotels', 'start_booking_year', validate.validated_count_hotel)


@bot.message_handler(state=MyStates.start_booking_year)
def start_bot_get_booking_month(message: Message):
    user_state.validate_data_and_proceed(message, 'start_booking_year', 'start_booking_month',
                                         validate.validated_start_year)


@bot.message_handler(state=MyStates.start_booking_month)
def start_bot_get_start_booking_day(message: Message):
    user_state.validate_data_and_proceed(message, 'start_booking_month', 'start_booking_day',
                                         validate.validated_start_month)


@bot.message_handler(state=MyStates.start_booking_day)
def bot_get_booking_year(message: Message):
    user_state.validate_data_and_proceed(message, 'start_booking_day', 'end_booking_year', validate.validated_start_day)


@bot.message_handler(state=MyStates.end_booking_year)
def start_bot_get_booking_month(message: Message):
    user_state.validate_data_and_proceed(message, 'end_booking_year', 'end_booking_month', validate.validated_end_year)


@bot.message_handler(state=MyStates.end_booking_month)
def start_bot_get_start_booking_day(message: Message):
    user_state.validate_data_and_proceed(message, 'end_booking_month', 'end_booking_day', validate.validated_end_month)


@bot.message_handler(state=MyStates.end_booking_day)
def bot_get_amount(message: Message):
    user_state.validate_data_and_proceed(message, 'end_booking_day', 'amount_people', validate.validated_end_day)


@bot.message_handler(state=MyStates.amount_people)
def ready_for_answer_or_get_price_range(message: Message):
    user_state.validate_data_and_proceed(message, 'amount_people', '', validate.validated_count_people)


@bot.message_handler(state=MyStates.price_range)
def get_distance_range(message: Message):
    user_state.validate_data_and_proceed(message, 'price_range', 'dist_range', validate.validated_price_range)


@bot.message_handler(state=MyStates.dist_range)
def get_show_photos(message: Message):
    user_state.validate_data_and_proceed(message, 'dist_range', 'show_photos', validate.validated_dist_range)


@bot.message_handler(state=MyStates.show_photos)
def get_count_photos(message: Message):
    user_state.validate_data_and_proceed(message, 'show_photos', 'count_photos', validate.validated_show_photos)


@bot.message_handler(state=MyStates.count_photos)
def ready_for_answer(message: Message):
    user_state.validate_data_and_proceed(message, 'count_photos', 'final', validate.validated_count_photos)


bot.add_custom_filter(custom_filters.StateFilter(bot))
