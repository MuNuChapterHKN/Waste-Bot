#!/usr/bin/env python3

from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext
import logging
import os
import re

# useless refactoring
import db

### Enable logging ###
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)  # you will know when (and why) things don't work as expected
logger = logging.getLogger(__name__)

TOKEN = os.environ['TOKEN']
# ADMIN_ID = os.environ['ADMIN_ID']

PHOTOCODE, ANSWER = range(2)

TRACKING = 50

### Messages ###
ask_barcode_msg = 'Perfetto! Inviami la foto del CODICE a barre. Premi "Annulla" se vuoi interrompere la conversazione.'
ask_photo_msg = 'Perfetto! Inviami la FOTO dell\'oggetto. Premi "Annulla" se vuoi interrompere la conversazione.'
barcode_msg = 'Perfetto! Inviami la foto del codice a barre.'
easter_barcode_msg = 'Questo CODICE è di un uovo di Pasqua. È corretto?'
easter_photo_msg = 'Questa FOTO è di un uovo di Pasqua. È corretto?'
help_msg = 'Comandi supportati:\n- \\start\n- \\help'
invalid_msg = 'Mi dispiace, non è una risposta valida. Operazione annullata'
photo_msg = 'Perfetto! Inviami la foto dell\'oggetto.'
undo_msg = 'Operazione annullata.'
unknown_command_msg = 'Mi dispiace, questo non è un comando supportato.'
unknown_message_msg = 'Mi dispiace, questa non è una risposta supportata al momento.'
waste_it_msg = 'Yeah! Allora buttalo nell\'indifferenziato, a presto!'
welcome_msg = 'Benvenuto nel Waste-Bot!\nCome vuoi riconoscere l\'oggetto?'
tracking_msg = 'Do you want to be tracked?'

### Keyboards ###
standard_keyboard = ReplyKeyboardMarkup([['Codice a barre', 'Foto']], resize_keyboard=True)
yesno_keyboard = ReplyKeyboardMarkup([['Si', 'No']], resize_keyboard=True)
undo_keyboard = ReplyKeyboardMarkup([['Annulla']], resize_keyboard=True)
no_keyboard = ReplyKeyboardRemove()

### Command handler functions ###
""" Definition of the functions associated with the command handlers """


def start(update: Update, _: CallbackContext):
    """Send a message when the command /start is issued."""
    user = update.message.from_user
    if (db.is_user(user.id)):
        update.message.reply_text(text='Bentornato, ' + user.username, reply_markup=standard_keyboard)
        return ConversationHandler.END
    else:
        # update.message.reply_text(text=welcome_msg, reply_markup=standard_keyboard)
        db.add_user(user.id, user.first_name, user.last_name, user.username)

        update.message.reply_text(text=tracking_msg, reply_markup=yesno_keyboard)

        return TRACKING


def track_away(update: Update, _:CallbackContext) -> int:
    db.change_user_tracking(update.message.from_user.id, True)

    update.message.reply_text("Bravo", reply_markup=standard_keyboard)
    return ConversationHandler.END


def dont_track(update: Update, _:CallbackContext) -> int:
    db.change_user_tracking(update.message.from_user.id, False)

    update.message.reply_text("mah", reply_markup=standard_keyboard)
    return ConversationHandler.END


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
""" Definition of the functions associated with the conversation handlers """


def ask_barcode(update: Update, _: CallbackContext) -> int:
    """Send a message when the command /code is issued asking for the barcode photo."""
    # user = update.message.from_user
    # logger.info("Modalita scelta of %s: %s", user.first_name, update.message.text)
    update.message.reply_text(text=ask_barcode_msg, reply_markup=undo_keyboard)
    return PHOTOCODE


def ask_photo(update: Update, _: CallbackContext) -> int:
    """Send a message when the command /photo is issued asking for the photo of the object."""
    # user = update.message.from_user
    # logger.info("Modalita scelta of %s: %s", user.first_name, update.message.text)
    update.message.reply_text(text=ask_photo_msg, reply_markup=undo_keyboard)
    return PHOTOCODE


def reply_barcode(update: Update, _: CallbackContext) -> int:
    """Sends a message in response to the barcode"""
    # user = update.message.from_user
    photo_file = update.message.photo[-1].get_file()
    photo_file.download('user_code.jpg')
    # logger.info("Codice of %s: %s", user.first_name, 'user_code.jpg')
    update.message.reply_text(text=easter_barcode_msg, reply_markup=yesno_keyboard)
    return ANSWER


def reply_photo(update: Update, _: CallbackContext) -> int:
    """Sends a message in response to the photo"""
    # user = update.message.from_user
    photo_file = update.message.photo[-1].get_file()
    photo_file.download('user_photo.jpg')
    # logger.info("Photo of %s: %s", user.first_name, 'user_photo.jpg')
    update.message.reply_text(text=easter_photo_msg, reply_markup=yesno_keyboard)
    return ANSWER


def last_reply(update: Update, _: CallbackContext) -> int:
    # user = update.message.from_user
    # logger.info("User location of %s", user.first_name)
    update.message.reply_text(text=waste_it_msg, reply_markup=standard_keyboard)
    return ConversationHandler.END


def undo(update: Update, _: CallbackContext) -> int:
    """Cancel the barcode or photo request"""
    # user = update.message.from_user
    # logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(text=undo_msg, reply_markup=standard_keyboard)
    return ConversationHandler.END


def invalid(update: Update, _: CallbackContext) -> None:
    """Send a message when the entered text is invalid."""
    # user = update.message.from_user
    # logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(text=invalid_msg, reply_markup=standard_keyboard)
    return ConversationHandler.END


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

    # User creation
    dispatcher.add_handler(
        ConversationHandler(
            entry_points=[CommandHandler('start', start)],
            states={
                TRACKING: [MessageHandler(Filters.regex(re.compile(r'si$', re.IGNORECASE)), track_away),
                            MessageHandler(Filters.regex(re.compile(r'no$', re.IGNORECASE)), dont_track)]
            },
            fallbacks=[]
        )
    )

    # Conversation handlers
    dispatcher.add_handler(
        ConversationHandler(
            entry_points=[CommandHandler('photo', ask_photo),
                          MessageHandler(Filters.regex(re.compile(r'^foto$', re.IGNORECASE)), ask_photo)],
            # responds to the /photo command or to the "Foto" button
            states={
                PHOTOCODE: [MessageHandler(Filters.photo, reply_photo),  # responds to the photo,
                            MessageHandler(Filters.regex(re.compile(r'^annulla$', re.IGNORECASE)), undo),
                            # responds toto the "Annulla" button
                            MessageHandler(Filters.text & ~Filters.command, invalid)],  # responds to invalid messages
                ANSWER: [MessageHandler(Filters.regex('^(Si|No)$'), last_reply),  # responds to the "Si|No" buttons
                         MessageHandler(Filters.text & ~Filters.command, invalid)],  # responds to invalid messages
            },
            fallbacks=[CommandHandler('cancel', undo),
                       MessageHandler(Filters.regex(re.compile(r'^annulla$', re.IGNORECASE)), undo)],
            # responds to the /cancel command or to the "Annulla" button
        )
    )

    dispatcher.add_handler(
        ConversationHandler(
            entry_points=[CommandHandler('code', ask_barcode),
                          MessageHandler(Filters.regex(re.compile(r'^codice a barre$', re.IGNORECASE)), ask_barcode)],
            # responds to the /code command or to the "Codice a barre" button
            states={
                PHOTOCODE: [MessageHandler(Filters.photo, reply_barcode),  # responds to the photo,
                            MessageHandler(Filters.regex(re.compile(r'^annulla$', re.IGNORECASE)), undo),
                            # responds toto the "Annulla" button
                            MessageHandler(Filters.text & ~Filters.command, invalid)],  # responds to invalid messages
                ANSWER: [MessageHandler(Filters.regex('^(Si|No)$'), last_reply),  # responds to the "Si|No" buttons
                         MessageHandler(Filters.text & ~Filters.command, invalid)],  # responds to invalid messages
            },
            fallbacks=[CommandHandler('cancel', undo),
                       MessageHandler(Filters.regex(re.compile(r'^annulla$', re.IGNORECASE)), undo)],
            # responds to the /cancel command or to the "Annulla" button
        )
    )

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
