import os
import aiohttp
from loguru import logger

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

from dotenv import load_dotenv
load_dotenv()

logger.add('gemini.log', rotation='1 month')


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
    logger.info("/start command received.")

# Обработчик команды /new
async def new_context(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response = "Начинаю новый контекст."
    await update.message.reply_text(response)
    logger.info("/new command received.")

# Обработчик текстовых сообщений
async def handle_text_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    max_length = 4096  # Максимальная длина сообщения в Telegram
    
    user_message = update.message.text
    chat_id = update.effective_chat.id
    
    await update.message.reply_text("Обрабатываю ваш запрос...")
    logger.info(f"Request: {user_message[:100]}")

    try:
        response = await b4a_gemini_response_(user_message)
        logger.info(f"Response: {response[:100]}")
        # await update.message.reply_text(response)
        for i in range(0, len(response), max_length):
            await context.bot.send_message(chat_id=chat_id, text=response[i:i + max_length])
            
    except Exception as e:
        await update.message.reply_text("Произошла ошибка при обработке вашего запроса.")
        logger.error(f"Error: {e}")


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
