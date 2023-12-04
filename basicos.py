# Responder a /start
def start_command(bot, message):
    bot.reply_to(message, '''🔹➖➖➖💠 * **Medina** * 💠➖➖➖🔹
  |   - Según las órdenes del Creador 
🔹 Mi deber es asistirte en lo que 
  |   necesites. A partir de hoy estoy 
🔹 totalmente disponible para ti. 
  |   Me encargaré de guiarte en tu viaje 
🔹 y ayudarte en tu recopilación 
  |   de la información! 
🔹- - - - - - -💠- - - - - - -🔹
  |   - En caso de ser requerida, usa el 
🔹 comando /help y te mostraré varias
  |   opciones que puedes tomar. 
🔹- - - - - - -💠- - - - - - -🔹
  |   - El Creador te desea una feliz 
🔹 estancia!
  | 
🔹➖➖➖➖💠........💠➖➖➖➖🔹
''', parse_mode='Markdown')
    
#Responder a /help
def help_command(bot, message):
    bot.reply_to(message, '''🔹➖➖➖💠 * **AYUDA** * 💠➖➖➖🔹
  |
🔹 /start - Mensaje de bienvenida
  |
🔹 /help - Esta ayuda
  |
🔹 /register - Registrar jugador
  |
🔹 /getinfo - Estadisticas de jugador
  |
🔹- - - - 💠**ADMINs**💠 - - - -🔹
  |
🔹 /adminmenu - Administración
  |
🔹 /opmenu - Desarrollo
  | 
🔹➖➖➖➖💠..FIN..💠➖➖➖➖🔹
''',parse_mode='Markdown')

# Responder a /opmenu
def opmenu_command(bot, message):
    user_id = message.from_user.id
    options_message = "🛠️ Opciones de Desarrollador v1.1:\n\n" \
        "/stats - Estadísticas de uso\n" \
        "/mantenimiento - Modo mantenimiento\n" \
        "/shutdown - Apagar bot\n" \
        "/notify - Enviar notificación a todos los administradores\n" \
        "/ads - Administrar anuncios (SIN IMPLEMENTAR)\n"
    bot.reply_to(message, options_message)

# Responder a /adminmenu
def adminmenu_command(bot, message):
    bot.reply_to(message, '''🔹➖➖➖💠 **Medina** 💠➖➖➖🔹
  |  Esto es todo por ahora:
🔹
  |
🔹 /notify - Notificar jugadores
  | 
🔹➖➖➖➖💠........💠➖➖➖➖🔹
''', parse_mode='Markdown')