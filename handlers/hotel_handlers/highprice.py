from telebot.types import Message

from states.user_state import start
from loader import bot, history


@bot.message_handler(commands=['highprice'])
def bot_highprice(message: Message):
    command_id = history.insert_command(message.from_user.id, 'highprice')
    start(message, 'highprice', command_id)


