from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, Filters, ConversationHandler
import re
from tempfile import NamedTemporaryFile
import os

import db
from common import *
from quickplagiarism import touch_of_code

(PHOTOCODE, CORRECTNESS, CATEGORIZATION) = range(3)

_photos_paths = dict()
# Dictionary of userID -> file path, to keep track of photos before deleting them or
# saving them if they are a fail


def undo(update: Update, _) -> int:
    """Cancel the barcode or photo request"""
    # user = update.message.from_user
    # logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(t('canceled', locale=lc(update)), reply_markup=standard_keyboard[lc(update)])
    return ConversationHandler.END


def invalid(update: Update, _) -> int:
    """Send a message when the entered text is invalid."""
    # user = update.message.from_user
    # logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(t('invalid message canceled', locale=lc(update)), reply_markup=standard_keyboard[lc(update)])
    return ConversationHandler.END


# Photo identification handlers
def ask_photo(update: Update, _) -> int:
    """Send a message when the command /photo is issued asking for the photo of the object."""
    # user = update.message.from_user
    # logger.info("Modalità scelta of %s: %s", user.first_name, update.message.text)
    update.message.reply_text(t('ask photo', locale=lc(update)), reply_markup=undo_keyboard[lc(update)])
    return PHOTOCODE


def reply_photo(update: Update, _) -> int:
    """Sends a message in response to the photo"""
    photo = update.message.photo[-1]
    photo_file = photo.get_file()

    # an hack
    my_temp_file = NamedTemporaryFile(suffix='.jpeg')
    my_temp_path = my_temp_file.name
    my_temp_file.close()

    photo_file.download(my_temp_path)
    # logger.info("Photo saved to %s e questa hack fa schifo", my_temp_path)

    ans = touch_of_code(my_temp_path)

    uid = update.message.from_user.id
    if uid in _photos_paths:
        os.remove(_photos_paths[uid])
    _photos_paths[update.message.from_user.id] = my_temp_path

    # logger.info("Photo of %s: %s", user.first_name, 'user_photo.jpg')
    update.message.reply_text(t('identified photo', label=t(ans, locale=lc(update)), locale=lc(update)),
                              reply_markup=yesno_keyboard[lc(update)])
    return CORRECTNESS


def get_photo_feedback(update: Update, _) -> int:
    m = update.message.text
    pattern = match_translations('yes', extras=['si'])
    if re.findall(pattern, m):
        update.message.reply_text(t('success', locale=lc(update)), reply_markup=standard_keyboard[lc(update)])
        os.remove(_photos_paths[update.message.from_user.id])
        del _photos_paths[update.message.from_user.id]
        return ConversationHandler.END
    else:
        update.message.reply_text(t('category question', locale=lc(update)),
                                  reply_markup=category_keyboard[lc(update)])
        return CATEGORIZATION


def categorize(update: Update, _) -> int:
    res = match_translations('cardboard', 'glass', 'metal', 'paper', 'plastic', 'trash')\
        .search(update.message.text).group()

    os.remove(_photos_paths[update.message.from_user.id])   # TODO: move to saved photos folder
    saved_path = "mimmo"
    del _photos_paths[update.message.from_user.id]
    db.save_fail(saved_path, category_from_translation(res))

    update.message.reply_text(t('feedback thanks', locale=lc(update)), reply_markup=standard_keyboard[lc(update)])
    return ConversationHandler.END


photoIdHandler = ConversationHandler(
    entry_points=[CommandHandler('photo', ask_photo),
                  MessageHandler(Filters.regex(match_translations('photo')), ask_photo)],
    # responds to the /photo command or to the "Foto" button
    states={
        PHOTOCODE: [
            MessageHandler(Filters.photo, reply_photo),  # responds to the photo,
            MessageHandler(Filters.regex(match_translations('cancel')), undo),
            # responds toto the "Annulla" button
            MessageHandler(Filters.text & ~Filters.command, invalid)],  # responds to invalid messages
        CORRECTNESS: [
            MessageHandler(Filters.regex(match_translations('yes', 'no', extras='si')), get_photo_feedback),  # responds to the "Si|No" buttons
            MessageHandler(Filters.text & ~Filters.command, invalid)],  # responds to invalid messages
        CATEGORIZATION: [
            MessageHandler(Filters.regex(match_translations('cardboard', 'glass', 'metal', 'paper', 'plastic', 'trash')),
                           categorize)
        ]
    },
    fallbacks=[CommandHandler('cancel', undo),
               MessageHandler(Filters.regex(match_translations('cancel')), undo)],
    # responds to the /cancel command or to the "Annulla" button
)


# Barcode identification
def ask_barcode(update: Update, _) -> int:
    """Send a message when the command /code is issued asking for the barcode photo."""
    # user = update.message.from_user
    # logger.info("Modalità scelta of %s: %s", user.first_name, update.message.text)
    update.message.reply_text(t('ask barcode', locale=lc(update)), reply_markup=undo_keyboard[lc(update)])
    return PHOTOCODE


def reply_barcode(update: Update, _) -> int:
    """Sends a message in response to the barcode"""
    # user = update.message.from_user
    photo_file = update.message.photo[-1].get_file()
    photo_file.download('user_code.jpg')
    # logger.info("Codice of %s: %s", user.first_name, 'user_code.jpg')
    update.message.reply_text(t('identified barcode', label='trash', locale=lc(update)), reply_markup=yesno_keyboard[lc(update)])
    return CORRECTNESS


# Only for the barcode
def last_barcode_reply(update: Update, _) -> int:
    # logger.info("User location of %s", user.first_name)
    update.message.reply_text(t('feedback thanks', locale=lc(update)), reply_markup=standard_keyboard[lc(update)])
    return ConversationHandler.END


barcodeHandler = ConversationHandler(
    entry_points=[CommandHandler('code', ask_barcode),
                  MessageHandler(Filters.regex(match_translations('barcode')), ask_barcode)],
    # responds to the /code command or to the "Codice a barre" button
    states={
        PHOTOCODE: [
            MessageHandler(Filters.photo, reply_barcode),  # responds to the photo,
            MessageHandler(Filters.regex(match_translations('cancel')), undo),
            # responds toto the "Annulla" button
            MessageHandler(Filters.text & ~Filters.command, invalid)],  # responds to invalid messages
        CORRECTNESS: [
            MessageHandler(Filters.regex(match_translations('yes', 'no', extras='si')), last_barcode_reply),  # responds to the "Si|No" buttons
            MessageHandler(Filters.text & ~Filters.command, invalid)],  # responds to invalid messages
    },
    fallbacks=[CommandHandler('cancel', undo),
               MessageHandler(Filters.regex(match_translations('cancel')), undo)],
    allow_reentry=True,
)
