# Bot library
import logging
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# Get the Telegram API token
import os
from dotenv import load_dotenv
load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


# Greet user
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[KeyboardButton('Nuevo Reporte')]]
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='¡Hola! Puedes reportar espacios seguros o peligrosos por medio de este bot.', 
        reply_markup=ReplyKeyboardMarkup(keyboard)
    )


# New report handler
async def new_report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = [[InlineKeyboardButton('Espacio seguro', callback_data='safe')],
               [InlineKeyboardButton('Espacio peligroso', callback_data='insecure')]]
    await context.bot.send_message(chat_id=update.effective_chat.id, text='¿Qué tipo de reporte?', reply_markup=InlineKeyboardMarkup(buttons))

# Main process
if __name__ == '__main__':

    # Start and set up the bot
    application = ApplicationBuilder().token(os.getenv('TOKEN')).build()
    
    # First time use, greet the user
    application.add_handler(CommandHandler('start', start))

    # Handle 'New Report' messages
    application.add_handler(MessageHandler(filters.TEXT, new_report))

    # Keep the bot listening for user input
    application.run_polling()
