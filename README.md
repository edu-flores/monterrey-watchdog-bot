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

