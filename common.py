from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
import logging

standard_keyboard = ReplyKeyboardMarkup([['Codice a barre', 'Foto']], resize_keyboard=True)
yesno_keyboard = ReplyKeyboardMarkup([['Si', 'No']], resize_keyboard=True)
undo_keyboard = ReplyKeyboardMarkup([['Annulla']], resize_keyboard=True)
no_keyboard = ReplyKeyboardRemove()

### Global logger ###
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)  # you will know when (and why) things don't work as expected
logger = logging.getLogger(__name__)
