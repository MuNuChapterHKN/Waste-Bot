import re

import telegram
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
import logging
import yaml

from quickplagiarism import CATEGORIES

### Global logger ###
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)  # you will know when (and why) things don't work as expected
logger = logging.getLogger(__name__)

with open('translations.yml') as transfile:
    _transdict = yaml.safe_load(transfile)


def t(key: str, locale: str, **fields) -> str:
    """
    Get the translation for the given key

    Args:
        key: Key of the translation (note: all keys must be defined in all locales
        locale: Locale of the user
        **fields: fields used for formatting the translation

    Returns:
        object: String in the right language, if formatting arguments are passed
    """
    if locale not in _transdict:
        locale = 'en'

    if key not in _transdict[locale]:
        raise KeyError(f"There is no translation for {key} in {locale}")

    if len(fields) == 0:
        return _transdict[locale][key]
    else:
        return _transdict[locale][key].format(**fields)


def lc(update: telegram.Update):
    """Returns the language code of the user that sent the message. Often used in conjunction with t"""
    return update.message.from_user.language_code


# Believe me it works and it's idiomatic even though it's unreadable
def _multilang_keyboard(butts):
    return {k: ReplyKeyboardMarkup([[t(text, locale=k) for text in buttonrow]
                                    for buttonrow in butts], resize_keyboard=True)
            for k in _transdict.keys()}


standard_keyboard = _multilang_keyboard([['barcode', 'photo']])
yesno_keyboard = _multilang_keyboard([['yes', 'no']])
undo_keyboard = _multilang_keyboard([['cancel']])
category_keyboard = _multilang_keyboard([['cardboard', 'glass', 'metal'], ['paper', 'plastic', 'trash']])
no_keyboard = ReplyKeyboardRemove()

_reverse_category = {_transdict[lc][c].upper(): c for lc in _transdict.keys() for c in CATEGORIES}


def category_from_translation(translation: str) -> str:
    return _reverse_category[translation.upper()]


def match_translations(*keys: str, extras=None) -> re.Pattern:
    """
    Generates a regex patter that matches all the translations for the provided keys

    Args:
        *keys: keys in the translations file as unnamed parameters
        extras: list of strings to be matched in addition to the translations

    Returns: regex pattern wanted

    """
    if extras is None:
        extras = []
    translations = [_transdict[l][key] for l in _transdict.keys() for key in keys]
    translations += extras

    # Concatenate all the translations into one regex pattern
    return re.compile("^(" + "|".join(translations) + ")$", re.IGNORECASE)