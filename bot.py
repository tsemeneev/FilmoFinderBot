from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import logging

from main import parser
from keyboards import get_seasons_keyboard


bot = Bot(token='YOUR_BOT_TOKEN')
dp = Dispatcher(bot)

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    filename='logs.log')


@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    await message.answer("Привет! Введи название фильма, а я его поищу")


@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def start_handler(message: types.Message):
    await message.answer("Ищем: " + message.text)

    film = parser.parse(message.text)
    if film:
        logging.info(f'Фильм: {film["title"]}')
        if 'seasons' in film.keys():
            keyboard = get_seasons_keyboard(film['seasons'])
            caption = film['title'] + '\n\n' + film['description']

            await bot.send_photo(chat_id=message.chat.id, photo=film['poster'], caption=caption, reply_markup=keyboard)
        else:
            photo = film['poster']
            caption = film['title'] + '\n\n' + film['description']
            keyboard = types.InlineKeyboardMarkup().add(
                types.InlineKeyboardButton(text='Смотреть онлайн', url=film['url']))
            await bot.send_photo(chat_id=message.chat.id, photo=photo, caption=caption, reply_markup=keyboard)
    else:
        await message.answer("К сожалению, ничего не найдено. Проверьте, пожалуйста, нет ли опечатки или попробуйте "
                             "вместе с названием указать год выпуска")


@dp.message_handler(content_types=[types.ContentTypes.ANY, types.ContentTypes.STICKER])
async def delete_flood(message: types.Message):
    await message.delete()
    await message.answer("Принимаю только текстовые сообщения")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
