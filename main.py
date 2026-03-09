import os
import logging
import sqlite3
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import Message

# Настройка логирования
logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.getenv("8746957458:AAGwxEJDKjlNVn9V2O1SSYCOsDkfe3t8k4k")

if not BOT_TOKEN:
    raise ValueError("Не найден BOT_TOKEN в переменных окружения Render!")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Имя файла базы данных
DB_NAME = "bot.db"

def init_db():
    """Инициализация базы данных SQLite"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Создаем таблицу, если она не существует
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id BIGINT UNIQUE NOT NULL,
            username TEXT,
            first_name TEXT,
            joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()
    logging.info("База данных SQLite инициализирована.")

# Хендлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: Message):
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    try:
        # Пробуем вставить пользователя. 
        # Если он уже есть (конфликт telegram_id), ничего не делаем или обновляем имя.
        cursor.execute("""
            INSERT OR IGNORE INTO users (telegram_id, username, first_name)
            VALUES (?, ?, ?)
        """, (user_id, username, first_name))
        
        if cursor.rowcount > 0:
            conn.commit()
            await message.answer(f"Привет, {first_name}! Ты успешно зарегистрирован в локальной базе.")
        else:
            await message.answer(f"С возвращением, {first_name}! Ты уже был в базе.")
            
    except Exception as e:
        logging.error(f"Ошибка БД: {e}")
        await message.answer("Произошла ошибка при работе с базой данных.")
    finally:
        conn.close()

# Хендлер на команду /stats (только для проверки работы БД)
@dp.message(Command("stats"))
async def cmd_stats(message: Message):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()[0]
    conn.close()
    
    await message.answer(f"Всего пользователей в базе: {count}")

# Запуск
async def main():
    # Инициализируем БД перед запуском поллинга
    init_db()
    logging.info("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
