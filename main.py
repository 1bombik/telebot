from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import requests
from cfg import TOKEN, api

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


class Weather:
    """Return current weather in Minsk"""

    @staticmethod
    def get_weather(city) -> str:
        r = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api}&units=metric')
        data = r.json()
        current_temp = data['main']['temp']
        return str(round(current_temp))


class Keyboard(Weather):
    """Create keyboard with buttons represents the city"""

    @staticmethod
    def keyboard() -> InlineKeyboardMarkup:
        keyboard = InlineKeyboardMarkup(row_width=1)
        but1 = InlineKeyboardButton(text='Минск', callback_data='Минск')
        but2 = InlineKeyboardButton(text='Гомель', callback_data='Гомель')
        but3 = InlineKeyboardButton(text='Гродно', callback_data='Гродно')
        but4 = InlineKeyboardButton(text='Витебск', callback_data='Витебск')
        but5 = InlineKeyboardButton(text='Могилёв', callback_data='Могилёв')
        but6 = InlineKeyboardButton(text='Брест', callback_data='Брест')
        keyboard.add(but1, but2, but3, but4, but5, but6)
        return keyboard

    @staticmethod
    @dp.message_handler(commands='weather')
    async def menu(message: types.Message):
        await message.answer(text='Выбери город:', reply_markup=Keyboard.keyboard())

    @staticmethod
    @dp.callback_query_handler()
    async def callback(callback: types.callback_query):
        if callback.data == 'Минск':
            return await callback.message.answer(f'Сейчас в Минске {Keyboard.get_weather("Минск")}')
        elif callback.data == 'Гомель':
            return await callback.message.answer(f'Сейчас в Гомеле {Keyboard.get_weather("Гомель")}')
        elif callback.data == 'Гродно':
            return await callback.message.answer(f'Сейчас в Гродно {Keyboard.get_weather("Гродно")}')
        elif callback.data == 'Витебск':
            return await callback.message.answer(f'Сейчас в Витебске {Keyboard.get_weather("Витебск")}')
        elif callback.data == 'Могилёв':
            return await callback.message.answer(f'Сейчас в Могилёве {Keyboard.get_weather("Могилёв")}')
        elif callback.data == 'Брест':
            return await callback.message.answer(f'Сейчас в Бресте {Keyboard.get_weather("Брест")}')


class Message:
    @staticmethod
    @dp.message_handler()
    async def message(message: types.Message):
        if message.text == message.text:
            await message.answer("Извини, друг, но я пока не умею воспринимать сообщения. \n"
                                 "Список доступных команд: \n"
                                 "/weather - узнать погоду в городе")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
