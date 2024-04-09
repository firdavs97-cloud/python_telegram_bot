from telebot.types import Message

from states.user_state import start
from loader import bot, history


@bot.message_handler(commands=['bestdeal'])
def bot_bestdeal(message: Message):
    command_id = history.insert_command(message.from_user.id, 'bestdeal')
    start(message, 'bestdeal', command_id)


