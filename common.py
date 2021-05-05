from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove

standard_keyboard = ReplyKeyboardMarkup([['Codice a barre', 'Foto']], resize_keyboard=True)
yesno_keyboard = ReplyKeyboardMarkup([['Si', 'No']], resize_keyboard=True)
undo_keyboard = ReplyKeyboardMarkup([['Annulla']], resize_keyboard=True)
no_keyboard = ReplyKeyboardRemove()
