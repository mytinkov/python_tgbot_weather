import asyncio
import requests
import datetime
from config import tgbot_token, open_weather_token
from aiogram import Bot, types
from aiogram.dispatcher.dispatcher import Dispatcher
from aiogram.filters import CommandStart, Command
import logging
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

dp = Dispatcher()

main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='moscow')
        ]
    ],
    resize_keyboard=True
)


@dp.message(CommandStart())
async def start_command(message: types.Message):
    await message.reply('Привет! Напиши мне название города и я пришлю сводку погоды!', reply_markup=main_kb)


@dp.message(Command('moscow'))
async def get_moscow_weather(message: types.Message):
    await get_weather()


@dp.message()
async def get_weather(message: types.Message):
    code_to_smile = {
        'Clear': 'Ясно \U00002600',
        'Clouds': 'Облачно \U00002601',
        'Rain': 'Дождь \U00002614',
        'Drizzle': 'Дождь \U00002614',
        'Thunderstorm': 'Гроза \U000026A1',
        'Snow': 'Снег \U0001F328',
        'Mist': 'Туман \U0001F32B',
    }

    try:
        r = requests.get(
            f'http://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric')
        data = r.json()

        city = data['name']
        cur_weather = data['main']['temp']

        weather_description = data['weather'][0]['main']
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = 'Посмотри в окно, не пойму что там происходит!'

        humidity = data['main']['humidity']
        sunrise_timestamp = datetime.datetime.fromtimestamp(
            data['sys']['sunrise'])  # Переводим из timestamp формата в читаемый вид
        sunset_timestamp = datetime.datetime.fromtimestamp(data['sys']['sunset'])
        length_of_the_day = sunset_timestamp - sunrise_timestamp

        await message.reply(f'*** {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")} ***\n'
                            f'Погода в городе: {city}\n'
                            f'Температура: {cur_weather}C° {wd}\n'
                            f'Влажность: {humidity}%\n'
                            f'Рассвет: {sunrise_timestamp}\n'
                            f'Закат: {sunset_timestamp}\n'
                            f'Продолжительность дня: {length_of_the_day}\n'
                            f'*** Хорошего дня ***!'
                            )

    except:
        await message.reply("\U00002620 Проверь название города \U00002620")


async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=tgbot_token, parse_mode='HTML')

    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")
