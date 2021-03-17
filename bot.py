#!/usr/bin/env python3

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import logging
import os
import re

### Enable logging ###
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)				# you will know when (and why) things don't work as expected
logger = logging.getLogger(__name__)

TOKEN = os.environ['TOKEN']
#ADMIN_ID = os.environ['ADMIN_ID']

### Messages ###
welcome_msg = 'Benvenuto nel Waste-Bot!\nCome posso esserti utile?'
barcode_msg = 'Perfetto! Inviami la foto del codice a barre.'
photo_msg = 'Perfetto! Inviami la foto dell\'oggetto.'
undo_msg = 'Operazione annullata.'
unknown_msg = 'Mi dispiace, questo non è un comando supportato.'
help_msg = 'Comandi supportati:\n- \\start\n- \\help'

### Keyboards ###
standard_keyboard = ReplyKeyboardMarkup([["Codice a barre"], ["Foto"]], resize_keyboard=True)
undo_keyboard = ReplyKeyboardMarkup([['Annulla']], resize_keyboard=True)

### Command handlers ###
""" Define a few command handlers. These usually take the two arguments update and context. Error handlers also receive the raised TelegramError object in error. """
def start(update: Update, _: CallbackContext) -> None:
	"""Send a message when the command /start is issued."""
	update.message.reply_text(text=welcome_msg, reply_markup=standard_keyboard)

def help_command(update: Update, _: CallbackContext) -> None:
	"""Send a message when the command /help is issued."""
	update.message.reply_text(text=help_msg, reply_markup=standard_keyboard)

def echo(update: Update, _: CallbackContext) -> None:
	"""Echo the user message."""
	update.message.reply_text(update.message.text, reply_markup=standard_keyboard)

def barcode(update: Update, _: CallbackContext) -> None:
	"""Sends a message asking for the barcode photo"""
	update.message.reply_text(text=barcode_msg, reply_markup=undo_keyboard)

def photo(update: Update, _: CallbackContext) -> None:
	"""Sends a message asking for the photo of the object"""
	update.message.reply_text(text=photo_msg, reply_markup=undo_keyboard)

def undo(update: Update, _: CallbackContext) -> None:
	"""Cancel the barcode or photo request"""
	update.message.reply_text(text=undo_msg, reply_markup=standard_keyboard)

def unknown(update, context):
	update.message.reply_text(text=unknown_msg, reply_markup=standard_keyboard)

### Main ###
def main() -> None:
	"""Start the bot."""
	# Create the Updater and pass it your bot's token.
	updater = Updater(TOKEN)

	# Get the dispatcher to register handlers
	dispatcher = updater.dispatcher

	# on different commands - answer in Telegram
	dispatcher.add_handler(CommandHandler("start", start))																			# responds to the /start command
	dispatcher.add_handler(CommandHandler("help", help_command))																	# responds to the /help command
	dispatcher.add_handler(MessageHandler(Filters.command, unknown))																# responds to any unknown command

	# on noncommand i.e message - echo the message on Telegram	
	dispatcher.add_handler(MessageHandler(Filters.regex(re.compile(r'^codice a barre$', re.IGNORECASE)), barcode))					# responds to the "Codice a barre" button
	dispatcher.add_handler(MessageHandler(Filters.regex(re.compile(r'^foto$', re.IGNORECASE)), photo))								# responds to the "Foto" button
	dispatcher.add_handler(MessageHandler(Filters.regex(re.compile(r'^annulla$', re.IGNORECASE)), undo))							# responds to the "Annulla" button
	dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

	# Start the Bot
	updater.start_polling()

	# Run the bot until you press Ctrl-C or the process receives SIGINT,
	# SIGTERM or SIGABRT. This should be used most of the time, since
	# start_polling() is non-blocking and will stop the bot gracefully.
	updater.idle()

if __name__ == '__main__':
	main()
