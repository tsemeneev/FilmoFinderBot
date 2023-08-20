from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_seasons_keyboard(seasons):
    seasons_keyboard = InlineKeyboardMarkup()
    for season in seasons:

        seasons_keyboard.add(InlineKeyboardButton(season['title'], url=season['url']))

    return seasons_keyboard
