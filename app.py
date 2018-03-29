import logging
import os
from queue import Queue
from threading import Thread
from telegram import Bot
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Updater, Filters
from jobs import start, get_gold, get_everyday
from actions import get_my_orders

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)
TOKEN = os.getenv('TOKEN')


def start(bot, update):
    update.message.reply_text('welcome MESSAGE')


def help(bot, update):
    update.message.reply_text('help message')


def echo(bot, update):
    update.message.reply_text(update.message.text)


def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"' % (update, error))

# Write your handlers here


def setup(webhook_url=None):
    """If webhook_url is not passed, run with long-polling."""
    logging.basicConfig(level=logging.WARNING)
    if webhook_url:
        bot = Bot(TOKEN)
        update_queue = Queue()
        dp = Dispatcher(bot, update_queue)
    else:
        updater = Updater(TOKEN)
        bot = updater.bot
        dp = updater.dispatcher
        dp.add_handler(CommandHandler("start", start))
        dp.add_handler(CommandHandler("help", help))
        dp.add_handler(CommandHandler("getgold", get_gold))
        dp.add_handler(CommandHandler("everyday", get_everyday))
        dp.add_handler(MessageHandler([Filters.text], get_my_orders))
        dp.add_handler(MessageHandler([Filters.group], get_my_orders))
        # on noncommand i.e message - echo the message on Telegram
        # dp.add_handler(MessageHandler(Filters.text, echo))

        # log all errors
        dp.add_error_handler(error)
    # Add your handlers here
    if webhook_url:
        bot.set_webhook(webhook_url=webhook_url)
        thread = Thread(target=dp.start, name='dispatcher')
        thread.start()
        return update_queue, bot
    else:
        bot.set_webhook()  # Delete webhook
        updater.start_polling()
        updater.idle()


if __name__ == '__main__':
    setup()
