<br>
<div align="center">
    <img width="50" src="https://pbs.twimg.com/profile_images/1436801567286611968/2zS5wmrz_400x400.jpg" alt="Logo">
    <h1>Chatbot de Seguridad</h1>
    <h3>Envío de reportes</h3>
</div>
<br>

## 💻 Para correr localmente:

1. Instalar dependencias con `pip install -r requirements.txt`.
2. Configurar un archivo `.env` con un token de Telegram API. 
3. Ejecutar `python main.py`.

<br>

## 🗂️ Explicación de archivos

* **.env.example** = Plantilla a seguir para crear el archivo `.env`.
* **.gitignore** = Configuración de git para ignorar ambientes virtuales y variables de entorno.
* **main.py** = La codificación del Chatbot en python.
* **README.md** = Documentación.
* **requierements.txt** = Librerías externas utilizadas en el código.

<br>

## 📱 Código

<br>

### General

Al inicio del programa, se importan módulos de la librería `python-telegram-bot`; esta se encarga de **recibir** y **enviar** los mensajes del Chatbot.

Las siguientes importaciones son para cargar variables de entorno. Con esto, se consigue el token para el *API* de Telegram.

También, se añade el módulo `logging` para tener registros de ejecución al correr programa.

<br>

### Librería "Python Telegram Bot"

<br>

#### Parámetros comúnes en los métodos

`update`: Es un objeto que contiene información sobre la última interacción que tuvo el bot con un usuario. Este objeto contiene información como el ID del chat, el mensaje que envió el usuario, el tipo de mensaje (texto, foto, audio, etc.) y otros detalles relevantes.

`context`: Es un objeto que contiene información adicional sobre la interacción actual, como por ejemplo la información del bot (su nombre de usuario, ID, etc.), información del chat (ID, tipo, etc.), información del usuario (ID, nombre, etc.) y otros datos relevantes.

<br>

#### Funciones adicionales

`context.bot.send_message`: Se usa para enviar mensajes. En los parámetros de este método se incluye el mensaje a enviar, el formato de este mismo, el teclado de respuesta a utilizar, etc.

`add_handler`: Se usa para agregar manejadores de eventos al bot, para saber *qué* responder a *qué* mensajes. Los manejadores pueden ser de texto, imagen, ubicación, etc.

<br>

### Métodos

Con estas funciones se maneja la leída y respuesta de mensajes por *Telegram*. Se puede utilizar lógica de *Python* dentro de estos métodos para obtener los resultados deseados.

`start`: Se obtiene la variable global *user*. El teclado se cambia a un botón para inicializar el proceso de un nuevo reporte, y se invita al usuario a comenzar.

`text_handler`: Se leen todos los mensajes de texto del usuario. Dependiendo de su respuesta, se envían los mensajes necesarios. En caso de no reconocer el mensaje, no se contesta nada.

`inline_handler`: Se encarga de leer la respuesta del menú entre líneas. Aquí se obtiene la variable global *report_type* para saber el tipo de reporte.

`location_handler`: Se encarga de leer ubicaciones enviadas por el usuario. Aquí se obtiene la variable global *report_location* para saber la ubicación del reporte.

`send_report`: Se muestra una recopilación de los datos obtenidos a lo largo de la conversación. Posteriormente, serán enviados a la base de datos.

<br>

### \_\_main__

Aquí inicia el proceso principal. Los pasos que se siguen son los siguientes:

1. Iniciar el bot con `ApplicationBuilder().token(os.getenv('TOKEN')).build()`. Se obtiene la variable de entorno `TOKEN`.
2. Agregar manejadores de texto, menús y ubicación al bot, con sus respectivos métodos.
3. Mantener el bot corriendo con `application.run_polling()`.
