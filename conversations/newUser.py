from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, Filters, ConversationHandler
import re

import db
from common import *

(TRACKINGID, STUDENTID) = range(2)


def start(update: Update, _) -> int:
    u = update.message.from_user
    if db.is_user(u.id):
        update.message.reply_text(t('welcome back', username=u.username, locale=lc(update)),
                                  reply_markup=standard_keyboard[lc(update)])
        return ConversationHandler.END

    db.add_user(u.id, u.first_name, u.last_name, u.username)
    update.message.reply_text(t('welcome back', username=u.username, locale=lc(update)), reply_markup=yesno_keyboard[lc(update)])
    return TRACKINGID


def privacy_settings(update: Update, _) -> int:
    update.message.reply_text(t('privacy settings', locale=lc(update)), reply_markup=yesno_keyboard[lc(update)])
    return TRACKINGID


def do_track(update: Update, _) -> int:
    u = update.message.from_user
    db.change_user_tracking(u.id, True)

    update.message.reply_text(t('student id question', locale=lc(update)), reply_markup=no_keyboard)
    return STUDENTID


def identify(update: Update, _) -> int:
    db.change_user_studentid(update.message.from_user.id,
                             re.findall(r's\d{6}', update.message.text)[0])
    update.message.reply_text(t('welcome aboard', username=update.message.from_user.username, locale=lc(update)),
                              reply_markup=standard_keyboard[lc(update)])
    return ConversationHandler.END


def id_fail(update: Update, _) -> int:
    update.message.reply_text(t('id fail', locale=lc(update)))

    return STUDENTID


def dont_track(update: Update, _) -> int:
    update.message.reply_text(t('not tracking', locale=lc(update)), reply_markup=standard_keyboard[lc(update)])
    db.change_user_tracking(update.message.from_user.id, False)
    db.change_user_studentid(update.message.from_user.id, "")

    return ConversationHandler.END


def trackingid_fallback(update: Update, _) -> int:
    update.message.reply_text(t('invalid yes or no', locale=lc(update)), reply_markup=yesno_keyboard[lc(update)])
    return TRACKINGID


newUserHandler = ConversationHandler(
    entry_points=[CommandHandler('start', start),
                  CommandHandler('ps', privacy_settings), CommandHandler('privacySettings', privacy_settings)],
    states={
        TRACKINGID: [MessageHandler(Filters.regex(match_translations('yes', extras='si')), do_track),
                     MessageHandler(Filters.regex(match_translations('no')), dont_track),
                     MessageHandler(Filters.all, trackingid_fallback)],
        STUDENTID: [MessageHandler(Filters.regex(re.compile(r's\d{6}', re.IGNORECASE)), identify),
                    MessageHandler(Filters.all, id_fail),
                    MessageHandler(Filters.command, id_fail)]
    },
    fallbacks=[]
)
