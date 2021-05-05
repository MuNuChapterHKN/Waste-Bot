#!/usr/bin/env python3

from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext
import logging
import os
import re

# functions to access db data
import db
from common import *

from conversations import *


### Enable logging ###
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)  # you will know when (and why) things don't work as expected
logger = logging.getLogger(__name__)

TOKEN = os.environ['TOKEN']
# ADMIN_ID = os.environ['ADMIN_ID']


### Messages ###
help_msg = 'Comandi supportati:\n- \\start\n- \\help'
photo_msg = 'Perfetto! Inviami la foto dell\'oggetto.'
unknown_command_msg = 'Mi dispiace, questo non è un comando supportato.'
unknown_message_msg = 'Mi dispiace, questa non è una risposta supportata al momento.'


def help_command(update: Update, _: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text(text=help_msg, reply_markup=standard_keyboard)


def echo(update: Update, _: CallbackContext) -> None:
    """Echo the user message."""
    update.message.reply_text(update.message.text, reply_markup=standard_keyboard)


def unknown_command(update, context):
    """Send a message when an unknown command is issued."""
    update.message.reply_text(text=unknown_command_msg, reply_markup=standard_keyboard)


def unknown_message(update, context):
    """Send a message when an unknown message is issued."""
    update.message.reply_text(text=unknown_message_msg, reply_markup=standard_keyboard)


### Conversation handler functions ###



### Main ###
def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Command handlers
    # dispatcher.add_handler(CommandHandler('start', start))  # responds to the /start command
    dispatcher.add_handler(CommandHandler('help', help_command))  # responds to the /help command

    dispatcher.add_handler(newUserHandler)
    dispatcher.add_handler(newUserHandler)
    dispatcher.add_handler(photoIdHandler)
    dispatcher.add_handler(barcodeHandler)

    # Last handlers
    dispatcher.add_handler(MessageHandler(Filters.command, unknown_command))  # responds to any unknown command
    dispatcher.add_handler(
        MessageHandler(Filters.text & ~Filters.command, unknown_message))  # responds to any unknown message

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
