import asyncio
import logging
import aiohttp
from aiogram import Bot, Dispatcher, F, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message

from config import TELEGRAM_TOKEN, AI_API_KEY

# Включаем логирование, чтобы видать всё, что происходит
logging.basicConfig(level=logging.INFO)

dp = Dispatcher()

# Функция отправки запроса к AI API
async def ask_ai(prompt: str) -> str:
    # URL для OpenRouter / OpenAI API
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {AI_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "openai/gpt-4o-mini", # При необходимости можно поменять модель
        "messages": [{"role": "user", "content": prompt}]
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return data["choices"][0]["message"]["content"]
                else:
                    error_text = await response.text()
                    return f"Ошибка API ({response.status}): {error_text}"
    except Exception as e:
        return f"Ошибка при подключении к AI: {e}"

# Обработка команды /start
@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Здорова! Я бот {html.bold('Arbuzov')}. Задавай любой вопрос, погнали!")

# Обработка всех обычных текстовых сообщений
@dp.message(F.text)
async def handle_message(message: Message) -> None:
    # Бот показывает индикатор «печатает...»
    await message.bot.send_chat_action(chat_id=message.chat.id, action="typing")
    
    # Получаем ответ от AI и отправляем пользователю
    ai_response = await ask_ai(message.text)
    await message.answer(ai_response)

async def main() -> None:
    bot = Bot(token=TELEGRAM_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот Arbuzov остановлен.")