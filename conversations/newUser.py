from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, Filters, ConversationHandler
import re

from database import crud
from common import t, lc, match_translations, standard_keyboard, yesno_keyboard, no_keyboard, undo_keyboard

(TRACKINGID, STUDENTID) = range(2)


def start(update: Update, _) -> int:
    u = update.message.from_user
    if crud.is_user(u.id):
        update.message.reply_text(t('welcome back', username=u.username, locale=lc(update)),
                                  reply_markup=standard_keyboard[lc(update)])
        return ConversationHandler.END

    crud.add_user(u.id)
    update.message.reply_text(t('welcome', username=u.username, locale=lc(update)), reply_markup=yesno_keyboard[lc(update)])
    return TRACKINGID


def privacy_settings(update: Update, _) -> int:
    update.message.reply_text(t('privacy settings', locale=lc(update)), reply_markup=yesno_keyboard[lc(update)])
    return TRACKINGID


def do_track(update: Update, _) -> int:
    update.message.reply_text(t('student id question', locale=lc(update)), reply_markup=undo_keyboard[lc(update)])

    return STUDENTID


def identify(update: Update, _) -> int:
    crud.user_enable_tracking(update.message.from_user.id,
                            re.findall(r's\d{6}', update.message.text)[0])
    update.message.reply_text(t('welcome aboard', username=update.message.from_user.username, locale=lc(update)),
                            reply_markup=standard_keyboard[lc(update)])
    return ConversationHandler.END


def id_fail(update: Update, _) -> int:
    update.message.reply_text(t('id fail', locale=lc(update)))

    return STUDENTID


def dont_track(update: Update, _) -> int:
    update.message.reply_text(t('not tracking', locale=lc(update)), reply_markup=standard_keyboard[lc(update)])
    crud.user_disable_tracking(update.message.from_user.id)

    return ConversationHandler.END


def trackingid_fallback(update: Update, _) -> int:
    update.message.reply_text(t('invalid yes or no', locale=lc(update)), reply_markup=yesno_keyboard[lc(update)])
    return TRACKINGID


newUserHandler = ConversationHandler(
    entry_points=[CommandHandler('start', start),
                  CommandHandler('ps', privacy_settings), CommandHandler('privacySettings', privacy_settings)],
    states={
        TRACKINGID: [MessageHandler(Filters.regex(match_translations('yes', extras=['si'])), do_track),
                     MessageHandler(Filters.regex(match_translations('no')), dont_track),
                     MessageHandler(Filters.all, trackingid_fallback)],
        STUDENTID: [MessageHandler(Filters.regex(re.compile(r's\d{6}', re.IGNORECASE)), identify),
                    MessageHandler(Filters.regex(match_translations('cancel')), privacy_settings),
                    MessageHandler(Filters.all, id_fail),
                    MessageHandler(Filters.command, id_fail)]
    },
    fallbacks=[]
)
