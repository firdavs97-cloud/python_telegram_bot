from telebot.types import Message

from states.user_state import start
from loader import bot, history


@bot.message_handler(commands=['lowprice'])
def bot_lowprice(message: Message):
    command_id = history.insert_command(message.from_user.id, 'lowprice')
    start(message, 'lowprice', command_id)