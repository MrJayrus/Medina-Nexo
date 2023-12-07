import telebot
import requests
import time
import threading
import datetime
import json
from functools import wraps
from basicos import *
from notificar import op_notify_command
from registrar_usuario import register_command
from obtener_datos import get_user_info_command

# Definir API del bot
bot = telebot.TeleBot('6044431859:AAHru48AtGHVDslBPOD8NwY3KrrNQr2NxME')

# Cargar base de datos de ids de usuarios local
with open('ids.json', 'r') as file:
    data = json.load(file)

# Variables
bot_activo = False
usage_count = 1
start_time = time.time()
id_file = 'ids.json'
maintenance_mode = True
usuario = data['users']
administrador = data['admins']
operador = data['ops']

# Función para manejar la reconexión
def reconnect():
    while bot_activo:
        try:
            # Intentar establecer la conexión
            bot.polling(none_stop=True)
            registrar_accion("Se está intentando establecer conexión con la API de Telegram...")
        except Exception as e:
            # Si ocurre un error, esperar un tiempo y volver a intentar
            print("Error de conexión:", e)
            time.sleep(5)  # Esperar 5 segundos antes de intentar nuevamente

    print("Bot a la escucha.")

# Iniciar la reconexión en un hilo separado
reconnect_thread = threading.Thread(target=reconnect)
reconnect_thread.start()

# Función para guardar la ID de un usuario
def save_user_id(user_id):
    if user_id not in usuario:
        usuario.append(user_id)
    # Guarda la lista actualizada en el archivo JSON
    # Crear el diccionario
    data = {
        "users": usuario,
        "admins": administrador,
        "ops": operador
    }
    with open(id_file, 'w') as file:
        json.dump(data, file)

def load_user_ids():
    with open(id_file, 'r') as file:
        data = json.load(file)
        usuario = data['users']
        administrador = data['admins']
        operador = data['ops']

# Función para verificar si un usuario es administrador
def is_admin(user_id):
    return user_id in administrador

# Función para verificar si un usuario es desarrollador
def is_op(user_id):
    return user_id in operador

# Registrar accion en el archivo registro.txt ubicado en la msma carpeta que este archivo
def registrar_accion(accion):
    fecha_hora_actual = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    mensaje_registro = f"{fecha_hora_actual} - {accion}\n"
    with open("registro.txt", "a", encoding='utf-8') as archivo_registro:
        archivo_registro.write(mensaje_registro)

# Función para verificar si el modo de mantenimiento está activado
def check_maintenance(func):
    @wraps(func)
    def wrapped(message):
        user_id = message.from_user.id
        if maintenance_mode and not is_admin(user_id):
            bot.reply_to(message, "No estoy de humor para ayudarte ahora mismo. Regresa más tarde.")
            return None
        return func(message)
    return wrapped

# Función para formatear el tiempo en días, horas, minutos y segundos
def format_time(seconds):
    time_delta = datetime.timedelta(seconds=seconds)
    days, seconds = time_delta.days, time_delta.seconds
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)
    return f"{days} días, {hours} horas, {minutes} minutos y {seconds} segundos"

# Función para incrementar usage_count y manejar el comando
def increment_usage_count(func):
    @wraps(func)
    def wrapped(message):
        global usage_count
        usage_count += 1
        func(message)
    return wrapped

# Manejar mensajes /mantenimiento
@bot.message_handler(commands=['mantenimiento'])
def handle_maintenance(message):
    user_id = message.from_user.id

    if user_id in operador:
        global maintenance_mode
        maintenance_mode = not maintenance_mode
        if maintenance_mode:
            bot.reply_to(message, "ℹ️ Modo de mantenimiento activado.")
            registrar_accion(f"Se activó el mantenimiento por el usuario: {user_id}")
        else:
            bot.reply_to(message, "ℹ️ Modo de mantenimiento desactivado.")
            registrar_accion(f"Se desactivó el mantenimiento por el usuario: {user_id}")
    else:
        bot.reply_to(message, "⚠️ No tienes permiso para activar o desactivar el modo de mantenimiento!")
        registrar_accion(f"El usuario: {user_id} trató de activar el modo mantenimiento")

# Manejar mensajes /stats
@bot.message_handler(commands=['stats'])
@increment_usage_count
def handle_stats(message):
    global start_time
    user_id = message.from_user.id
    current_time = time.time()
    uptime = current_time - start_time

    stats_message = f"📊 Estadísticas del Bot:\n\n" \
                    f"🔄 Veces usado: {usage_count}\n" \
                    f"⏳ Tiempo de actividad: {format_time(uptime)}\n" \
                    f"🛠️ Estado de mantenimiento: {maintenance_mode}\n" \
                    f"✏️ ID de Usuario: {user_id}"

    bot.reply_to(message, stats_message)
    registrar_accion(f"Se mostraron las estadísticas para el usuario: {user_id}")

# Manejar mensajes /shutdown con confirmación
@bot.message_handler(commands=['shutdown'])
def handle_shutdown(message):
    user_id = message.from_user.id

    if user_id in operador:
        # Pedir confirmación al usuario antes de apagar el bot
        confirmation_markup = telebot.types.InlineKeyboardMarkup()
        confirm_button = telebot.types.InlineKeyboardButton(text="Sí, apagar", callback_data="confirm_shutdown")
        cancel_button = telebot.types.InlineKeyboardButton(text="Cancelar", callback_data="cancel_shutdown")
        confirmation_markup.row(confirm_button, cancel_button)

        confirmation_message = "⚠️ ¿Estás seguro de que deseas apagar el bot? Esta acción no se puede deshacer."

        bot.send_message(message.chat.id, confirmation_message, reply_markup=confirmation_markup)
    else:
        bot.reply_to(message, "⚠️ No tienes permiso para apagar el bot.")

# Manejar la confirmación del apagado
@bot.callback_query_handler(func=lambda call: True)
def handle_shutdown_confirmation(call):
    user_id = call.from_user.id

    if user_id in operador:
        if call.data == "confirm_shutdown":
            bot.delete_message(call.message.chat.id, call.message.message_id)
            bot.send_message(call.message.chat.id, "⚠️ Apagando bot.")
            bot.stop_polling()
            print("Bucle de escucha detenido por comando de apagado (/shutdown)")
        elif call.data == "cancel_shutdown":
            bot.delete_message(call.message.chat.id, call.message.message_id)
            bot.send_message(call.message.chat.id, "⚠️ Apagado cancelado.")
    else:
        bot.answer_callback_query(call.id, text="⚠️ No tienes permiso para realizar esta acción!")
# INICIO DEL RESTO DEL CODIGO

# Manejar mensajes /start
@bot.message_handler(commands=['start'])
@check_maintenance
@increment_usage_count
def handle_start(message):
    start_command(bot, message)
    save_user_id(message.from_user.id)
    user_id = message.from_user.id
    registrar_accion(f"Se mostró START para el usuario: {user_id}")

# Manejar mensajes /help
@bot.message_handler(commands=['help'])
@check_maintenance
@increment_usage_count
def handle_help(message):
    help_command(bot, message)
    save_user_id(message.from_user.id)
    user_id = message.from_user.id
    registrar_accion(f"Se mostró HELP para el usuario: {user_id}")

# Manejar mensajes /register
@bot.message_handler(commands=['register'])
@check_maintenance
@increment_usage_count
def handle_register(message):
    register_command(bot, message)
    save_user_id(message.from_user.id)
    user_id = message.from_user.id
    registrar_accion(f"Se mostró RegisteR para el usuario: {user_id}")

# Manejar mensajes /getinfo
@bot.message_handler(commands=['getinfo'])
@check_maintenance
@increment_usage_count
def handle_getinfo(message):
    get_user_info_command(bot, message)
    save_user_id(message.from_user.id)
    user_id = message.from_user.id
    registrar_accion(f"Se mostró GetinfO para el usuario: {user_id}")

# Manejar mensajes /razas
@bot.message_handler(commands=['razas'])
@check_maintenance
@increment_usage_count
def handle_razas(message):
    razas_command(bot, message)
    save_user_id(message.from_user.id)
    user_id = message.from_user.id
    registrar_accion(f"Se mostró razas para el usuario: {user_id}")

# Manejar mensajes /adminmenu
@bot.message_handler(commands=['amenu']) # type: ignore
@check_maintenance
def handle_amenu(message):
    adminmenu_command(bot, message)
    save_user_id(message.from_user.id)
    user_id = message.from_user.id
    registrar_accion(f"Se mostró adminmenu para el usuario: {user_id}")

# Manejar mensajes /adminmenu
@bot.message_handler(commands=['notify'])
def handle_notify(message):
    save_user_id(message.from_user.id)
    user_id = message.from_user.id
    if is_op(message.from_user.id):
        registrar_accion(f"El operador: {user_id} quiere enviar un mensaje a los administradores")
        users_to_send = administrador
        op_notify_command(bot, message, users_to_send)
    elif is_admin(message.from_user.id):
        registrar_accion(f"El administrador: {user_id} quiere enviar un mensaje a los usuarios")
        users_to_send = usuario
        op_notify_command(bot, message, users_to_send)
    else:
        registrar_accion(f"Se denego NOTIFY para el usuario: {user_id}")
        bot.reply_to(message, "⚠️ No tienes permiso para realizar esta acción!")

# Manejar comando /OPMENU
@bot.message_handler(commands=['opmenu'])
def handle_opmenu(message):
    save_user_id(message.from_user.id)
    user_id = message.from_user.id
    if is_op(message.from_user.id):
        registrar_accion(f"Se mostró OPMENU para el usuario: {user_id}")
        opmenu_command(bot, message)
    else:
        registrar_accion(f"Se denego OPMENU para el usuario: {user_id}")
        bot.reply_to(message, "⚠️ No tienes permiso para realizar esta acción!")

# FINAL DEL RESTO DEL CODIGO
bot.polling(none_stop=True)