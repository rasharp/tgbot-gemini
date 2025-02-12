import os
import asyncio

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from google import genai

# from dotenv import load_dotenv
# load_dotenv()


# Читаем переменные окружения
TGBOT_API_TOKEN = os.environ.get('TGBOT_API_TOKEN', '')
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', '')

# Функция для работы с моделью
def gemini_wrapper():
    # client = genai.Client(api_key=GEMINI_API_KEY)

    # async def get_gemini_response(prompt):
    #     response = await client.aio.models.generate_content(
    #                         model='gemini-2.0-flash',
    #                         contents="Write a story about a magic dragonfly.")
    #     return response.text

    async def get_test_response(prompt):
        return "Really! I don't think so..."

    return get_test_response


gemini_response = gemini_wrapper()


# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response = "Привет! Я бот, который может отвечать на ваши вопросы, используя модель Gemini. Напишите мне что-нибудь!"
    await update.message.reply_text(response)

# Обработчик команды /new
async def new_context(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response = "Начинаю новый контекст."
    await update.message.reply_text(response)

# Обработчик текстовых сообщений
async def handle_text_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    await update.message.reply_text("Обрабатываю ваш запрос...")
    try:
        response = await gemini_response(user_message)
        await update.message.reply_text(response)
    except Exception as e:
        await update.message.reply_text("Произошла ошибка при обработке вашего запроса.")
        print(f"Error: {e}")

# Основная функция для запуска бота
def main():
    # Создание экземпляра приложения
    application = ApplicationBuilder().token(TGBOT_API_TOKEN).build()

    # Регистрация обработчиков
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("new", new_context))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_message))

    # Запуск бота
    application.run_polling()


if __name__ == '__main__':
    main()