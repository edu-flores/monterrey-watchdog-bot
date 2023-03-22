# Librería para el bot de Telegram
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup, constants
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, CallbackQueryHandler, filters

# Obtener el token guardado para el bot
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


# Desplegar instrucciones de funcionamiento al usuario
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # Conseguir el nombre del usuario
    global user
    user = update.effective_user.first_name

    # Mostrar lista de comandos disponibles
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=('Te puedo ayudar a enviar un registro de _seguridad_ o _criminalidad_, '
              'dentro del área de Monterrey\.\n'
              '\n'
              '*Comandos*\n'
              '/start \- Mostrar instrucciones\n'
              '/registro \- Comenzar un nuevo registro\n'
              '/cancelar \- Detener registro actual\n'
              '\n'
              'Presiona el botón ☰ al lado izquierdo del cuadro de texto para abrir '
              'el menú de comandos\.'),
        parse_mode=constants.ParseMode.MARKDOWN_V2
    )


# Manejador de textos simples
async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # Propiedades
    message, markup, reply = None, None, None

    # Mostrar menú textual para seleccionar el tipo de reporte
    if 'Nuevo reporte' in update.message.text:
        message = '¿Qué tipo de reporte?'
        buttons = [[InlineKeyboardButton('💐 Espacio seguro', callback_data='safe')], [InlineKeyboardButton('⚠️ Espacio peligroso', callback_data='insecure')]]
        markup = InlineKeyboardMarkup(buttons)
        reply = update.message.message_id

    # Confirmar
    elif 'Aceptar' in update.message.text:
        message = 'Reporte enviado exitosamente.'
        reply = update.message.message_id
        markup = ReplyKeyboardRemove()
        # send_report()

    # Denegar
    elif 'Cancelar' in update.message.text:
        message = 'Reporte cancelado.'
        reply = update.message.message_id
        markup = ReplyKeyboardRemove()

    # Cualquier otro mensaje, no hacer nada
    else:
        return

    # Enviar la respuesta con las propiedades necesarias
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=message,
        reply_markup=markup,
        reply_to_message_id=reply
    )


# Manejador de inline menus
async def inline_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # Obtener la respuesta del menu textual
    query = update.callback_query
    data = query.data

    # Obtener el tipo de reporte
    global report_type
    report_type = 'seguridad' if data == 'safe' else 'peligro'

    # Solicitar al usuario a enviar una ubicación
    await query.answer(text=('Ha seleccionado: Reporte de ' + report_type))
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f'Para completar el reporte de {report_type}, seleccione el ícono 📎 y posteriormente envíe la ubicación 📌 del reporte.'
    )


# Manejador de ubicaciones
async def location_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # Obtener latitud y longitud
    latitude = update.message.location.latitude
    longitude = update.message.location.longitude

    # Obtener ubicación
    global report_location
    report_location = [latitude, longitude]

    # Preguntar por confirmación
    keyboard = [[KeyboardButton('👍 Aceptar')], [KeyboardButton('👎 Cancelar')]]
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f'Usted ha enviado un reporte de {report_type}, en la ubicación {report_location}. ¿Confirma estos datos?',
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )


# Enviar datos a la BD
def send_report():
    print(f'User: {user}. \nReport type: {report_type}. \nLocation: {report_location}. \nTimestamp: {int(timestamp)}.')

# Proceso principal
if __name__ == '__main__':

    # Inicializar y configurar el bot
    application = ApplicationBuilder().token(os.getenv('TOKEN')).build()

    # Añadir manejadores de comandos
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('registro', register))
    application.add_handler(CommandHandler('cancelar', cancel))

    # Manejar mensajes de texto
    application.add_handler(MessageHandler(filters.TEXT, text_handler))

    # Manejar inline menus
    application.add_handler(CallbackQueryHandler(inline_handler))

    # Manejar ubicaciones
    application.add_handler(MessageHandler(filters.LOCATION, location_handler))

    # Mantener al bot activo y escuchando nuevas peticiones
    application.run_polling()
