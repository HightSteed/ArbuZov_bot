import asyncio
import logging
import os
import sys
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

# Получаем токен из переменных окружения Render
TOKEN = os.getenv("TELEGRAM_TOKEN")

if not TOKEN:
    print("Ошибка: Не задан TELEGRAM_TOKEN в переменных окружения!")
    sys.exit(1)

# Инициализируем бота
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Здарова! Бот Арбузов успешно запущен и работает.")

async def main():
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    print("Запуск бота...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
