import os
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from supabase import create_client, Client

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация переменных
BOT_TOKEN = os.getenv("BOT_TOKEN")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Проверка наличия переменных
if not all([BOT_TOKEN, SUPABASE_URL, SUPABASE_KEY]):
    raise ValueError("Не найдены переменные окружения! Проверьте настройки в Render.")

# Инициализация бота и Supabase
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Хендлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username
    
    try:
        # Пытаемся сохранить пользователя в базу
        data = supabase.table("users").insert({
            "telegram_id": user_id,
            "username": username
        }).execute()
        
        logging.info(f"Пользователь {user_id} сохранен в БД")
        await message.answer(f"Привет, @{username}! Я сохранил тебя в базе данных Supabase.")
        
    except Exception as e:
        logging.error(f"Ошибка при записи в БД: {e}")
        # Если пользователь уже есть, Supabase может выдать ошибку уникальности (зависит от настроек)
        await message.answer("Привет! Что-то пошло не так с базой данных, но я работаю.")

# Функция запуска
async def main():
    logging.info("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())