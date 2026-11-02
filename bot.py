import asyncio
import logging
import os
import sys
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import google.generativeai as genai

# Получаем ключи из переменных окружения Render
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
AI_API_KEY = os.getenv("AI_API_KEY")

if not TELEGRAM_TOKEN:
    print("Ошибка: Не задан TELEGRAM_TOKEN!")
    sys.exit(1)

# Настраиваем Gemini API, если ключ задан
if AI_API_KEY:
    genai.configure(api_key=AI_API_KEY)
    # Используем актуальную модель Gemini
    ai_model = genai.GenerativeModel("gemini-2.5-flash")
else:
    ai_model = None
    print("Предупреждение: Не задан AI_API_KEY, ИИ-функции будут отключены.")

bot = Bot(token=TELEGRAM_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

# Создаем клавиатуру с кнопками из интерфейса бота
main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📊 Статистика"), KeyboardButton(text="🔔 Режим Фокуса")],
        [KeyboardButton(text="⚡ Быстрые Шаблоны"), KeyboardButton(text="⏰ Напоминания")]
    ],
    resize_keyboard=True
)

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "Здарова! Бот Арбузов успешно запущен и готов к работе. Выбирай нужную функцию на клавиатуре или просто пиши свой вопрос сюда — я отвечу через ИИ!",
        reply_markup=main_keyboard
    )

# Обработка нажатий на кнопки
@dp.message(F.text == "📊 Статистика")
async def btn_stats(message: types.Message):
    await message.answer("📊 Раздел статистики: здесь будет отображаться вся информация и прогресс.")

@dp.message(F.text == "🔔 Режим Фокуса")
async def btn_focus(message: types.Message):
    await message.answer("🔔 Режим фокуса активирован. Уведомления временно приглушены.")

@dp.message(F.text == "⚡ Быстрые Шаблоны")
async def btn_templates(message: types.Message):
    await message.answer("⚡ Выбери нужный быстрый шаблон или создай новый.")

@dp.message(F.text == "⏰ Напоминания")
async def btn_reminders(message: types.Message):
    await message.answer("⏰ Список твоих активных напоминаний пуст.")

# Обработка любых других текстовых сообщений через Gemini AI
@dp.message(F.text)
async def handle_ai_message(message: types.Message):
    if not ai_model:
        await message.answer(f"Ты написал: {message.text} (ИИ-ключ не настроен)")
        return

    # Показываем, что бот думает
    await bot.send_chat_action(chat_id=message.chat.id, action="typing")
    try:
        response = ai_model.generate_content(message.text)
        await message.answer(response.text)
    except Exception as e:
        await message.answer(f"Произошла ошибка при обращении к ИИ: {e}")

async def main():
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    print("Запуск бота со всеми функциями и ИИ...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
