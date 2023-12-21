import json
from config import *

# Responder a /start
def start_command(bot, message):
    bot.reply_to(message, start_message, parse_mode='Markdown')
    
#Responder a /help
def help_command(bot, message):
    bot.reply_to(message, help_message,parse_mode='Markdown')

# Responder a /opmenu
def opmenu_command(bot, message):
    user_id = message.from_user.id
    options_message = op_menu_message
    bot.reply_to(message, options_message)

# Responder a /adminmenu
def adminmenu_command(bot, message):
    bot.reply_to(message, admin_menu_message, parse_mode='Markdown')

def razas_command(bot, message):
    user_id = message.from_user.id
    bot.send_message(user_id, "Aquí está la lista completa de razas:")
    for raza in razas:
        bot.send_message(user_id, f"{raza['Nombre']}: {raza['Detalle']}")