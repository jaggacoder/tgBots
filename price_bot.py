TOKEN = ''
import requests
from bs4 import BeautifulSoup
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters

updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher

import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def start(bot, update):
	welcome_text = "Hello {0}, send me some text!".format(str(update.message.chat.first_name))
	bot.send_message(chat_id=update.message.chat_id, text=welcome_text)

def link(bot, update):
	link = update.message.text
	result = requests.get(link)
	soup = BeautifulSoup(result.text, "html.parser")
	str = soup.find(id = 'priceblock_ourprice').text
	str = str.replace(',', '');
	price = float(str)
	while True:
		bot.send_message(chat_id=update.message.chat_id, text=price)
		if price < 2400.0:
			bot.send_message(chat_id=update.message.chat_id, text=price)
		time.sleep(300)

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

link_handler = MessageHandler(Filters.text, link)
dispatcher.add_handler(link_handler)

updater.start_polling()
updater.idle()