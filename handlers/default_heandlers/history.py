from telebot.types import Message

from loader import bot, history


@bot.message_handler(commands=['history'])
def bot_history(message: Message):
    data = history.display(message.from_user.id)
    bot.reply_to(message, "Ранее введенные команды:\n"
                          f"{data}")
