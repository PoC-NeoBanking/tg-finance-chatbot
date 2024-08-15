import asyncio
import json
import os
import re

from aiogram import Bot, Dispatcher, types
from aiogram import Router
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command
from dotenv import load_dotenv

from olama_function import translate_and_generate_response

# Завантаження змінних середовища
load_dotenv()

# Отримання токена API з змінної середовища
API_TOKEN = os.getenv('BOT_TOKEN')
CONTEXT_FILE = 'context.json'

# Ініціалізація бота з властивостями за замовчуванням
bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
router = Router()

# Словник для зберігання стану обробки для кожного користувача
processing_flags = {}

def format_message(text: str) -> str:
    """Перетворення тексту зі знаками ** і * на HTML-теги для Telegram."""
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)  # Жирний текст
    text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)      # Курсивний текст
    return text


def load_context():
    """Завантаження контексту з файлу."""
    if os.path.exists(CONTEXT_FILE):
        with open(CONTEXT_FILE, 'r') as f:
            return json.load(f)
    return {}


def save_context(context):
    """Збереження контексту у файл."""
    with open(CONTEXT_FILE, 'w') as f:
        json.dump(context, f)


# Обробник команди /start
@router.message(Command('start'))
async def StartCommand(message: types.Message):
    await message.reply("Привіт!\nЯ ваш фінансовий експерт-асистент.\n"
                        "Напишіть мені будь-яке питання, що стосується теми фінансів, "
                        "і я постараюся дати відповідь!")


# Обробник всіх текстових повідомлень (для обробки запитів)
@router.message()
async def handle_message(message: types.Message):
    user_id = message.from_user.id

    if processing_flags.get(user_id, False):
        # Якщо запит вже обробляється для цього користувача, відповідаємо йому
        await message.reply("Будь ласка, зачекайте, поки обробляється ваш попередній запит.")
    else:
        # Інакше запускаємо обробку запиту
        processing_flags[user_id] = True
        asyncio.create_task(process_message(message))


async def process_message(message: types.Message):
    user_id = message.from_user.id
    user_context = load_context()

    # Відправлення повідомлення про те, що запит обробляється
    waiting_message = await message.reply("Запит почав оброблятися, будь ласка, почекайте...")

    # Отримання контексту для поточного користувача
    context = user_context.get(str(user_id), "")

    # Виклик асинхронної функції для перекладу та генерації відповіді
    answer, new_context = await translate_and_generate_response(message.text, context)

    formatted_answer = format_message(answer)

    # Оновлення повідомлення результатом
    await waiting_message.edit_text(f"Ваша відповідь:\n{formatted_answer}")

    # Оновлення контексту для поточного користувача
    user_context[str(user_id)] = new_context

    # Збереження контексту у файл
    save_context(user_context)

    # Зняття флагу обробки
    processing_flags[user_id] = False


# Головна функція для запуску бота
async def main():
    # Очищення вебхуків
    await bot.delete_webhook(drop_pending_updates=True)

    # Реєстрація обробників
    dp.include_router(router)

    # Запуск полінгу для обробки вхідних повідомлень
    await dp.start_polling(bot)


if __name__ == '__main__':
    # Запуск асинхронної функції
    asyncio.run(main())
