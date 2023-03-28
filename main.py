# Librería para el bot de Telegram
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup, constants
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, CallbackQueryHandler, filters

# Librería para la conexión a la base de datos
import pyodbc

# Obtener el token guardado para el bot
import os
from dotenv import load_dotenv
load_dotenv()

# Misc
from time import time
import logging

# Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Conectar con la base de datos
conn = pyodbc.connect("Driver={MySQL ODBC 8.0 ANSI Driver};"
                      "Server=localhost;"
                     f"Database={os.getenv('DATABASE')};"
                     f"User={os.getenv('USER')};"
                     f"Password={os.getenv('PASSWORD')};"
                      "Port=3306;")
cursor = conn.cursor()

user, record_type, record_location = None, None, None

# Desplegar instrucciones de funcionamiento al usuario
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

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

    global user

    # Si ya hay un registro en proceso, regresar
    if user:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=('Ya hay un registro en proceso. 😅')
        )
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=('Para cancelar el registro actual, use el comando /cancelar.')
        )
        return

    # Conseguir el nombre del usuario
    user = update.effective_user.first_name

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

    # Elegir mensaje
    global user, record_type, record_location
    message = 'Registro cancelado.' if user else 'No hay un registro en proceso. 🤔'

    # Notificar al usuario del cancelamiento
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=message,
        reply_markup=ReplyKeyboardRemove()
    )

    # Restaurar variables globales
    user, record_type, record_location = None, None, None


# Manejador de textos simples
async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # Propiedades
    message, reply, markup = None, None, None
    global user, record_type

    # Solicitar al usuario su ubicación a partir del tipo de registro
    if ('Registro de seguridad' in update.message.text or 'Registro de criminalidad' in update.message.text) and user:
        message = 'Bien, ahora seleccione el ícono 📎 y posteriormente envíe la ubicación 📌 del registro.'
        reply = update.message.message_id
        markup = ReplyKeyboardRemove()

        # Obtener el tipo de registro
        record_type = 'seguridad' if 'Registro de seguridad' in update.message.text else 'criminalidad'

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

    global record_type, record_location

    # Si no se ha seleccionado un tipo, regresar
    if not record_type:
        return

    # Obtener latitud y longitud
    latitude = update.message.location.latitude
    longitude = update.message.location.longitude

    # Obtener ubicación
    record_location = [latitude, longitude]

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Ubicación recibida.',
        reply_to_message_id=update.message.message_id
    )

    # Mostrar datos enviados por el usuario
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=('*Resumen*\n'
              '\n'
             f'Tipo: _{record_type}_\n'
             f'Ubicación: [ver mapa](https://www.google.com/maps/search/?api=1&query={latitude},{longitude})'),
        parse_mode=constants.ParseMode.MARKDOWN_V2
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

    # Informar al usuario de su decisión de confirmación
    accepted = data == 'accept'
    await query.answer(text=('🕐 Procesando...'))
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Registro ' + ('enviado' if accepted else 'detenido') + ' exitosamente.'
    )

    # Quitar el inline menu
    await query.edit_message_reply_markup(None)

    # Enviar datos en caso de haber aceptado
    if accepted:
        send_record()

    # Mandar información extra de contacto
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=('Si gustas ponerte en contacto con nosotras\.\.\.\n'
              '*Correo:* georregias@gmail\.com\n'
              '*Instagram:* [@georregias](https://www.instagram.com/georregias/)\n'
              '*Facebook:* [Georregias](https://www.facebook.com/Georregias)\n'
              '\n'
              '¡Envíanos un mensaje o correo y platiquemos\! 💜'),
        parse_mode=constants.ParseMode.MARKDOWN_V2,
        disable_web_page_preview=True
    )

    # Restaurar variables globales
    global user, record_type, record_location
    user, record_type, record_location = None, None, None


# Enviar datos a la BD
def send_record():
    timestamp = time()
    print(f'User: {user}. \nRecord type: {record_type}. \nLocation: {record_location}. \nTimestamp: {int(timestamp)}.')

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

    # Cerrar conexión a la base de datos al terminar
    conn.close()
