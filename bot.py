import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from dotenv import load_dotenv

# 1. Загружаем переменные из файла .env
load_dotenv()

# 2. Получаем токен из переменной окружения
# Если токена нет, программа выдаст ошибку, а не упадет с непонятным сообщением
TOKEN = os.getenv("8746957458:AAGwxEJDKjlNVn9V2O1SSYCOsDkfe3t8k4k")

if not TOKEN:
    print("❌ Ошибка: Токен не найден! Проверьте файл .env")
    exit(1)

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()

# --- Обработчики команд ---

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    """Реагирует на команду /start"""
    await message.answer(
        f"👋 Привет, {message.from_user.first_name}!\n"
        "Я безопасный бот, написанный на Python.\n"
        "Мой токен надежно спрятан в файле .env."
    )

@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    """Реагирует на команду /help"""
    await message.answer("Я умею отвечать на команду /start и эхо-сообщения.")

# --- Обработчик обычных сообщений (Эхо) ---

@dp.message()
async def echo_handler(message: types.Message):
    """Отвечает тем же текстом на любое сообщение"""
    if message.text:
        await message.answer(f"🔊 Эхо: {message.text}")

# --- Запуск бота ---

async def main():
    print("✅ Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n⛔ Бот остановлен пользователем.")
