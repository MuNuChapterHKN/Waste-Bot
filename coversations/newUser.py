from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CommandHandler, MessageHandler, Filters, ConversationHandler
from enum import Enum, auto
import re

import db
from common import *

(TRACKINGID, STUDENTID) = range(2)


def start(update: Update, _) -> int:
    u = update.message.from_user
    if db.is_user(u.id):
        update.message.reply_text(f"Bentornato {u.username}", reply_markup=standard_keyboard)
        return ConversationHandler.END

    db.add_user(u.id, u.first_name, u.last_name, u.username)
    update.message.reply_text(text="Do you want to be tracked?", reply_markup=yesno_keyboard)
    return TRACKINGID


def do_track(update: Update, _) -> int:
    u = update.message.from_user
    db.change_user_tracking(u.id, True)

    update.message.reply_text(text="What is your user id?", reply_markup=no_keyboard)
    return STUDENTID


def identify(update: Update, _) -> int:
    # Add to db
    update.message.reply_text("Welcome aboard " + update.message.text)
    return ConversationHandler.END


def id_fail(update: Update, _) -> int:
    update.message.reply_text(text="The id is not valid, try again")

    return STUDENTID


def dont_track(update: Update, _) -> int:
    update.message.reply_text("Ok, do as you wish")

    return END


newUserHandler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        TRACKINGID: [MessageHandler(Filters.regex(re.compile(r'si$', re.IGNORECASE)), do_track),
                     MessageHandler(Filters.regex(re.compile(r'no$', re.IGNORECASE)), dont_track)],
        STUDENTID: [MessageHandler(Filters.regex(re.compile(r's\d{6}', re.IGNORECASE)), identify),
                    MessageHandler(Filters.all, id_fail)]
    },
    fallbacks=[]
)
