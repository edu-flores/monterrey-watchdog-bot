# Bot library
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

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
    await context.bot.send_message(chat_id=update.effective_chat.id, text='¡Hola! Puedes reportar espacios seguros o peligrosos por medio de este bot.')

# Main process
if __name__ == '__main__':

    # Start and set up the bot
    application = ApplicationBuilder().token(os.getenv('TOKEN')).build()
    
    # First time use, greet the user
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    # Keep the bot listening for user input
    application.run_polling()
