from telebot import TeleBot
from telebot.storage import StateMemoryStorage
from config_data import config
from database.mysql import MysqlDB

history = MysqlDB(config.MYSQL_CREDS['database'])
storage = StateMemoryStorage()
bot = TeleBot(token=config.BOT_TOKEN, state_storage=storage)

