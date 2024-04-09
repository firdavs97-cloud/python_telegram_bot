from telebot.handler_backends import State, StatesGroup  # States


# States group.
class MyStates(StatesGroup):
    city = State()
    count_hotels = State()
    start_booking_year = State()
    start_booking_month = State()
    start_booking_day = State()
    end_booking_year = State()
    end_booking_month = State()
    end_booking_day = State()
    amount_people = State()
    price_range = State()
    dist_range = State()
    show_photos = State()
    count_photos = State()

