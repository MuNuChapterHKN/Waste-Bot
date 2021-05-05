from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CommandHandler, MessageHandler, Filters, ConversationHandler
import re
from tempfile import NamedTemporaryFile
import os

import db
from common import *
from quickplagiarism import touch_of_code

(PHOTOCODE, CORRECTNESS) = range(2)


undo_msg = 'Operazione annullata.'
invalid_msg = 'Mi dispiace, non è una risposta valida. Operazione annullata'
ask_photo_msg = 'Perfetto! Inviami la FOTO dell\'oggetto. Premi "Annulla" se vuoi interrompere la conversazione.'
waste_it_msg = 'Yeah! Allora buttalo nell\'indifferenziato, a presto!'
ask_barcode_msg = 'Perfetto! Inviami la foto del CODICE a barre. Premi "Annulla" se vuoi interrompere la conversazione.'
easter_photo_msg = 'Questa FOTO è di un uovo di Pasqua. È corretto?'
easter_barcode_msg = 'Questa BARCODE è di un uovo di Pasqua. È corretto?'


# For both (atm)
def last_reply(update: Update, _) -> int:
    # user = update.message.from_user
    # logger.info("User location of %s", user.first_name)
    update.message.reply_text(text=waste_it_msg, reply_markup=standard_keyboard)
    return ConversationHandler.END


def undo(update: Update, _) -> int:
    """Cancel the barcode or photo request"""
    # user = update.message.from_user
    # logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(text=undo_msg, reply_markup=standard_keyboard)
    return ConversationHandler.END


def invalid(update: Update, _) -> int:
    """Send a message when the entered text is invalid."""
    # user = update.message.from_user
    # logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(text=invalid_msg, reply_markup=standard_keyboard)
    return ConversationHandler.END


# Photo identification handlers
def ask_photo(update: Update, _) -> int:
    """Send a message when the command /photo is issued asking for the photo of the object."""
    # user = update.message.from_user
    # logger.info("Modalita scelta of %s: %s", user.first_name, update.message.text)
    update.message.reply_text(text=ask_photo_msg, reply_markup=undo_keyboard)
    return PHOTOCODE


def reply_photo(update: Update, _) -> int:
    """Sends a message in response to the photo"""
    # user = update.message.from_user
    photo = update.message.photo[-1]
    photo_file = photo.get_file()
    # get_prediction(photo_file.download_as_bytearray(), (photo.width, photo.height))

    # an hack
    my_temp_file = NamedTemporaryFile(suffix='.jpeg')
    my_temp_path = my_temp_file.name
    my_temp_file.close()

    photo_file.download(my_temp_path)
    # logger.info("Photo saved to %s e questa hack fa schifo", my_temp_path)

    ans = touch_of_code(my_temp_path)

    os.remove(my_temp_path)
    # logger.info("Photo of %s: %s", user.first_name, 'user_photo.jpg')
    # update.message.reply_text(text=easter_photo_msg, reply_markup=yesno_keyboard)
    update.message.reply_text(text="Hai inviato " + ans + ", giusto?", reply_markup=yesno_keyboard)
    return CORRECTNESS


photoIdHandler = ConversationHandler(
    entry_points=[CommandHandler('photo', ask_photo),
                  MessageHandler(Filters.regex(re.compile(r'^foto$', re.IGNORECASE)), ask_photo)],
    # responds to the /photo command or to the "Foto" button
    states={
        PHOTOCODE: [
            MessageHandler(Filters.photo, reply_photo),  # responds to the photo,
            MessageHandler(Filters.regex(re.compile(r'^annulla$', re.IGNORECASE)), undo),
            # responds toto the "Annulla" button
            MessageHandler(Filters.text & ~Filters.command, invalid)],  # responds to invalid messages
        CORRECTNESS: [
            MessageHandler(Filters.regex('^(Si|No)$'), last_reply),  # responds to the "Si|No" buttons
            MessageHandler(Filters.text & ~Filters.command, invalid)],  # responds to invalid messages
    },
    fallbacks=[CommandHandler('cancel', undo),
               MessageHandler(Filters.regex(re.compile(r'^annulla$', re.IGNORECASE)), undo)],
    # responds to the /cancel command or to the "Annulla" button
)


# Barcode identification
def ask_barcode(update: Update, _) -> int:
    """Send a message when the command /code is issued asking for the barcode photo."""
    # user = update.message.from_user
    # logger.info("Modalita scelta of %s: %s", user.first_name, update.message.text)
    update.message.reply_text(text=ask_barcode_msg, reply_markup=undo_keyboard)
    return PHOTOCODE


def reply_barcode(update: Update, _) -> int:
    """Sends a message in response to the barcode"""
    # user = update.message.from_user
    photo_file = update.message.photo[-1].get_file()
    photo_file.download('user_code.jpg')
    # logger.info("Codice of %s: %s", user.first_name, 'user_code.jpg')
    update.message.reply_text(text=easter_barcode_msg, reply_markup=yesno_keyboard)
    return CORRECTNESS


barcodeHandler = ConversationHandler(
    entry_points=[CommandHandler('code', ask_barcode),
                  MessageHandler(Filters.regex(re.compile(r'^codice a barre$', re.IGNORECASE)), ask_barcode)],
    # responds to the /code command or to the "Codice a barre" button
    states={
        PHOTOCODE: [
            MessageHandler(Filters.photo, reply_barcode),  # responds to the photo,
            MessageHandler(Filters.regex(re.compile(r'^annulla$', re.IGNORECASE)), undo),
            # responds toto the "Annulla" button
            MessageHandler(Filters.text & ~Filters.command, invalid)],  # responds to invalid messages
        CORRECTNESS: [
            MessageHandler(Filters.regex('^(Si|No)$'), last_reply),  # responds to the "Si|No" buttons
            MessageHandler(Filters.text & ~Filters.command, invalid)],  # responds to invalid messages
    },
    fallbacks=[CommandHandler('cancel', undo),
               MessageHandler(Filters.regex(re.compile(r'^annulla$', re.IGNORECASE)), undo)],   # responds to the /cancel command or to the "Annulla" button
)
