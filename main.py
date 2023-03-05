# Bot library
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, CallbackQueryHandler, filters

# Get the Telegram API token
import os
from dotenv import load_dotenv
load_dotenv()

# Misc
from time import time
import logging

timestamp = time()
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


# Greet user
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global user
    user = update.effective_user.first_name
    keyboard = [[KeyboardButton('Nuevo Reporte')]]
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='¡Hola! Puedes reportar espacios seguros o peligrosos por medio de este bot.', 
        reply_markup=ReplyKeyboardMarkup(keyboard)
    )


# New report handler
async def new_report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = [[InlineKeyboardButton('Espacio seguro', callback_data='safe')], [InlineKeyboardButton('Espacio peligroso', callback_data='insecure')]]
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='¿Qué tipo de reporte?',
        reply_markup=InlineKeyboardMarkup(buttons)
    )


# Pick safe or insecure report
async def select_type(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    global report_type
    report_type = 'seguridad' if data == 'safe' else 'peligro'
    await query.answer(text=('Ha seleccionado: Reporte de ' + report_type))
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f'Para completar el reporte de {report_type}, seleccione el ícono 📎 y posteriormente envíe la ubicación 📍 del reporte.'
    )


# Pick report location
async def select_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    latitude = update.message.location.latitude
    longitude = update.message.location.longitude
    global report_location
    report_location = [latitude, longitude]
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f'Tu latitud es {latitude}, y longitud es {longitude}.'
    )
    send_report()


# Send data to DB
def send_report():
    print(f'User: {user}. \nReport type: {report_type}. \nLocation: {report_location}. \nTimestamp: {timestamp}.')

# Main process
if __name__ == '__main__':

    # Start and set up the bot
    application = ApplicationBuilder().token(os.getenv('TOKEN')).build()
    
    # First time use, greet the user
    application.add_handler(CommandHandler('start', start))

    # Handle 'New Report' messages
    application.add_handler(MessageHandler(filters.TEXT, new_report))

    # Select which type of report
    application.add_handler(CallbackQueryHandler(select_type))

    # Handle report location
    application.add_handler(MessageHandler(filters.LOCATION, select_location))

    # Keep the bot listening for user input
    application.run_polling()
