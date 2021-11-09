#!/usr/bin/env python3

from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import os

from database.database import Base, engine

from common import t, lc, standard_keyboard
from conversations import newUserHandler, photoIdHandler, barcodeHandler


TOKEN = os.environ['TOKEN']
# ADMIN_ID = os.environ['ADMIN_ID']


def help_command(update: Update, _: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text(t('help', locale=lc(update)), reply_markup=standard_keyboard[lc(update)])


def unknown_command(update: Update, _):
    """Send a message when an unknown command is issued."""
    update.message.reply_text(text=t('unknown command', locale=lc(update)), reply_markup=standard_keyboard[lc(update)])


def unknown_message(update: Update, _):
    """Send a message when an unknown message is issued."""
    update.message.reply_text(text=t('invalid msg', locale=lc(update)), reply_markup=standard_keyboard[lc(update)])


# Main
def main() -> None:
    Base.metadata.create_all(bind=engine)

    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    dispatcher.add_handler(newUserHandler)
    dispatcher.add_handler(newUserHandler)
    dispatcher.add_handler(photoIdHandler)
    dispatcher.add_handler(barcodeHandler)

    # Command handlers
    # dispatcher.add_handler(CommandHandler('start', start))  # responds to the /start command
    dispatcher.add_handler(CommandHandler('help', help_command))  # responds to the /help command

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
