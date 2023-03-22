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


# Comenzar un nuevo registro
async def register(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # Notificar al usuario del comienzo
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Entendido, comenzemos.'
    )

    # Preguntar tipo de registro
    keyboard = [[KeyboardButton('🦺 Registro de seguridad')], [KeyboardButton('⛔ Registro de criminalidad')]]
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='¿Qué tipo de registro desea enviar?',
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )


# Detener registro actual
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # Notificar al usuario del cancelamiento
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Registro cancelado.'
    )


# Manejador de textos simples
async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # Propiedades
    message, reply, markup = None, None, None

    # Solicitar al usuario su ubicación a partir del tipo de registro
    if 'Registro de seguridad' in update.message.text or 'Registro de criminalidad' in update.message.text:
        message = 'Bien, ahora seleccione el ícono 📎 y posteriormente envíe la ubicación 📌 del registro.'
        reply = update.message.message_id
        markup = ReplyKeyboardRemove()

    # Cualquier otro mensaje, no hacer nada
    else:
        return

    # Enviar la respuesta con las propiedades necesarias
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=message,
        reply_to_message_id=reply,
        reply_markup=markup
    )


# Manejador de ubicaciones
async def location_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # Obtener latitud y longitud
    latitude = update.message.location.latitude
    longitude = update.message.location.longitude

    # Obtener ubicación
    global report_location
    report_location = [latitude, longitude]

    # Mostrar ubicación enviada por el usuario
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Ubicación recibida.',
        reply_to_message_id=update.message.message_id
    )

    # Preguntar por confirmación
    buttons = [[InlineKeyboardButton('✅ Aceptar', callback_data='accept')], [InlineKeyboardButton('❌ Rechazar', callback_data='decline')]]
    markup = InlineKeyboardMarkup(buttons)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='¿Desea confirmar este registro?',
        reply_markup=markup
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

    # Manejar ubicaciones
    application.add_handler(MessageHandler(filters.LOCATION, location_handler))

    # Manejar inline menus
    application.add_handler(CallbackQueryHandler(inline_handler))

    # Mantener al bot activo y escuchando nuevas peticiones
    application.run_polling()
