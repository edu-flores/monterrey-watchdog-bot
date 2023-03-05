# Bot library
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
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

    # Get username
    global user
    user = update.effective_user.first_name

    # Set custom keyboard and start the convo
    keyboard = [[KeyboardButton('Nuevo reporte 📄')]]
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='¡Hola! Puedes reportar espacios seguros o peligrosos de Monterrey por medio de este bot.', 
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )


# New report handler
async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # Props
    message, markup, reply = None, None, None

    if 'Nuevo reporte' in update.message.text:
        # Show inline menu to select the report type
        message = '¿Qué tipo de reporte?'
        buttons = [[InlineKeyboardButton('Espacio seguro 💐', callback_data='safe')], [InlineKeyboardButton('Espacio peligroso ⚠️', callback_data='insecure')]]
        markup = InlineKeyboardMarkup(buttons)
        reply = update.message.message_id

    elif 'Aceptar' in update.message.text:
        message = 'Reporte enviado exitosamente.'
        reply = update.message.message_id
        markup = ReplyKeyboardRemove()

    elif 'Cancelar' in update.message.text:
        message = 'Reporte cancelado.'
        reply = update.message.message_id
        markup = ReplyKeyboardRemove()

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=message,
        reply_markup=markup,
        reply_to_message_id=reply
    )


# Pick safe or insecure report
async def inline_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # Get inline menu option
    query = update.callback_query
    data = query.data

    # Get report type
    global report_type
    report_type = 'seguridad' if data == 'safe' else 'peligro'

    # Prompt user to send a location
    await query.answer(text=('Ha seleccionado: Reporte de ' + report_type))
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f'Para completar el reporte de {report_type}, seleccione el ícono 📎 y posteriormente envíe la ubicación 📍 del reporte.'
    )


# Pick report location
async def location_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # Get latitude and longitude
    latitude = update.message.location.latitude
    longitude = update.message.location.longitude

    # Get location
    global report_location
    report_location = [latitude, longitude]

    # Ask for confirmation
    keyboard = [[KeyboardButton('Aceptar 👍')], [KeyboardButton('Cancelar 👎')]]
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f'Usted ha enviado un reporte de {report_type}, en la ubicación {report_location}. ¿Confirma estos datos?',
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )
    send_report()


# Send data to DB
def send_report():
    print(f'User: {user}. \nReport type: {report_type}. \nLocation: {report_location}. \nTimestamp: {int(timestamp)}.')

# Main process
if __name__ == '__main__':

    # Start and set up the bot
    application = ApplicationBuilder().token(os.getenv('TOKEN')).build()
    
    # First time use, greet the user
    application.add_handler(CommandHandler('start', start))

    # Handle text messages for 'New report' and confirmations
    application.add_handler(MessageHandler(filters.TEXT, text_handler))

    # Select which type of report
    application.add_handler(CallbackQueryHandler(inline_handler))

    # Handle report location
    application.add_handler(MessageHandler(filters.LOCATION, location_handler))

    # Keep the bot listening for user input
    application.run_polling()
