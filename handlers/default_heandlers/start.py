from telebot.types import Message

from handlers.default_heandlers.help import bot_help
from loader import bot, history
from utils.set_bot_commands import set_hotel_commands


@bot.message_handler(commands=['start'])
def bot_start(message: Message):
    history.insert_command(message.from_user.id, 'start')
    set_hotel_commands(bot)
    bot.delete_state(message.from_user.id, message.chat.id)
    bot_help(message)


