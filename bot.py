import os
import aiohttp

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# from dotenv import load_dotenv
# load_dotenv()


# Читаем переменные окружения
TGBOT_API_TOKEN = os.environ.get('TGBOT_API_TOKEN', '')

B4A_APP_ID = os.environ.get('B4A_APP_ID', '')
B4A_API_KEY = os.environ.get('B4A_API_KEY', '')
URL = "https://parseapi.back4app.com/functions/gemini"

async def b4a_gemini_response_(prompt):
    headers = {
        "X-Parse-Application-Id": B4A_APP_ID,
        "X-Parse-REST-API-Key": B4A_API_KEY,
        "Content-Type": "application/json"
    }
    
    json_data = {
        "prompt": prompt
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(URL, headers=headers, json=json_data) as response:
            response_data = await response.json()
            return response_data['result']['candidates'][0]['content']['parts'][0]['text']
        

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
        response = await b4a_gemini_response_(user_message)
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