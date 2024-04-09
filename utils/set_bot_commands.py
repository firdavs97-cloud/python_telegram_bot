from telebot.types import BotCommand
from config_data.config import DEFAULT_COMMANDS, HOTEL_COMMANDS, STATE_COMMANDS


def set_default_commands(bot):
    commands = DEFAULT_COMMANDS
    bot_commands = [BotCommand(*i) for i in commands]
    bot.set_my_commands(bot_commands)


def set_hotel_commands(bot):
    commands = DEFAULT_COMMANDS + HOTEL_COMMANDS
    bot_commands = [BotCommand(*i) for i in commands]
    bot.set_my_commands(bot_commands)


def set_state_commands(bot):
    commands = DEFAULT_COMMANDS + HOTEL_COMMANDS + STATE_COMMANDS
    bot_commands = [BotCommand(*i) for i in commands]
    bot.set_my_commands(bot_commands)
