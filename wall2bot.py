"""
# wall2bot

This is a Telegram bot that gets a random image using the unsplash.com API
and sends it to the user.

Insert the information in the following variables to get the bot to work:

- TOKEN
    Telegram bot token received from @botfather on telegram.
- unsplash_app_name
    the name of your app registered at unsplash.com api.
- parameters
    Get the client_id from unsplash api.


## Dependencies:

$ pip install requests python-telegram-bot

## Run it as:

$ python wall2bot.py

It's working as @wall2bot on Telegram currently.
Link: http://t.me/wall2bot
"""

import json
import logging
import requests
import sys
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - \
                    %(message)s', level=logging.INFO)

"""
Insert your telegram bot token here.
If you don't have one, then get it from @botfather bot on telegram.
"""
TOKEN = ""

# Exit if no token specified.
if TOKEN == "":
    print("\nInsert your API tokens and other information first!\n")
    exit()
updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher


def start(bot, update):
    """Action on /start command.

    On the first start of the bot, /start command is automatically sent.  So
    the following code will always run at least once.
    """
    welcome_text = "Hello {0}, click on /random to get a random wallpaper."\
        .format(update.message.chat.first_name)
    bot.send_message(chat_id=update.message.chat_id, text=welcome_text)

def help(bot, update):
    """Action on /help command.

    The /help command can be used for getting some help when the user feels
    lost.
    """
    update.message.reply_text("Use command /random to get a random wallpaper.")

def echo(bot, update):
    """Echoes the message in caps.

    Send the bot any text message and it will SHOUT the same text (in caps).
    """

    # If user sends a sticker, then reply this.
    if bool(update.message.sticker) is True:
        caps_message = "/random :P"
    else:
        caps_message = update.message.text.upper()
    bot.send_message(chat_id=update.message.chat_id, text=caps_message)

def get_image(bot, update):
    """Gets a random image from unsplash.com with /random command.

    Uses the unsplash api and gets the random image from the api. It also
    includes the reference of author's name (with unsplash profile link) and
    unsplash website as the caption of the image.
    """

    # Insert your app name, registered with unsplash API, e.g. wallpaperz.
    unsplash_app_name = ""

    """Insert your unsplash api token (client_id) here.
    Get yours at https://unsplash.com/developers. It should look something
    like this:
    parameters = {"client_id": "98lsjdfjjslfjl28329...43ulfjs9d8f7s89df7s9d9"}
    """
    parameters = {"client_id": ""}
    # if no client_id specified, then /random command won't work.
    if parameters['client_id'] == "":
        error_message = "You forgot to mention the Unsplash API token."
        print(error_message)
        bot.send_message(chat_id=update.message.chat_id, text=error_message)
    # API call for the random image.
    response = requests.get("https://api.unsplash.com/photos/random",
                            params=parameters).json()
    # Getting image link from the response.
    image_link = response['urls']['regular']
    # Link to Author's profile on Unsplash.
    author_profile = response['user']['links']['html']
    # Photographer/Author's name.
    author_name = response['user']['name']
    # Needed to refer back to unsplash.
    unsplash_referral = "?utm_source={0}&utm_medium=referral"\
        .format(unsplash_app_name)
    author = "<a href='{0}{2}'>{1}</a>"\
        .format(author_profile, author_name, unsplash_referral)
    # Unsplash.com link.
    unsplash = "<a href='https://unsplash.com{0}'>Unsplash</a>"\
        .format(unsplash_referral)
    # Caption under the photo giving attribution to the photographer.
    caption = "Photo by {0} on {1}".format(author, unsplash)
    # Send the photo with HTML caption.
    bot.send_photo(update.message.chat_id, image_link, caption,
                   parse_mode='HTML')
    # update.message.reply_photo(image_link)

# Start command.
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

# Help command.
help_handler = CommandHandler('help', help)
dispatcher.add_handler(help_handler)

# Filters regular messages and stickers and calls echo function.
echo_handler = MessageHandler(Filters.text|Filters.sticker, echo)
dispatcher.add_handler(echo_handler)

# Random command.
get_image_handler = CommandHandler('random', get_image)
dispatcher.add_handler(get_image_handler)

# Start the bot.
updater.start_polling()

# Keep running until SIGINT, SIGTERM or SIGABRT signals are received.
updater.idle()
