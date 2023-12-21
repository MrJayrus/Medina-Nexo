import telebot
import requests
from functools import wraps

# Comando para enviar notificaciones a usuarios
def op_notify_command(bot, message, users_to_send):
    bot.reply_to(message, "Escriba el mensaje que desea enviar a los usuarios:")
    bot.register_next_step_handler(message, notify_op, users_to_send, bot)

# Función para enviar notificaciones
def notify_op(message, users_to_send, bot):
    notification_message = message.text
    send_notification_to_users(bot, users_to_send, notification_message)
    bot.reply_to(message, f"Se envió la notificación a {len(users_to_send)} usuarios.")

# Función para enviar una notificación a usuarios
def send_notification_to_users(bot, users_to_send, notification_message):
    for user_id in users_to_send:
        try:
            bot.send_message(user_id, notification_message)
        except Exception as e:
            # Manejar excepciones si falla el envío a un usuario específico
            print(f"No se pudo enviar la notificación a {user_id}: {str(e)}")