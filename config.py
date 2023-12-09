import json
import telebot
import time

# Cargar la base de datos de los ID
with open('ids.json', 'r') as file:
    data = json.load(file)

# Cargar razas desde la base de datos
with open('razas_db.json', 'r', encoding='utf-8') as file:
    razas = json.load(file)
    
# Definir API del bot
bot = telebot.TeleBot('6044431859:AAHru48AtGHVDslBPOD8NwY3KrrNQr2NxME')

# Variables
bot_activo = False
usage_count = 1
start_time = time.time()
id_file = 'ids.json'
maintenance_mode = True
players_db = 'players.json'
usuario = data['users']
administrador = data['admins']
operador = data['ops']

# Variables con textos largos
razas_del_registro = """🔹➖➖💠 Medina 💠➖➖🔹
- Elija su raza acorde a las características especificadas por el Creador:
🔹- - - - - - - - -💠- - - - - - - - -🔹
⚔️ Continente Innombrado:
- `Humano De Las LLamas`
- `Humano de la luz`
- `Humano Lunar`
- `Humano Fantasma`
- `Humano del Viento`
- `Humano Reforzado`
- `Humano de la Noche`
- `Humano Escarcha`
- `Humano Versátil`
- `Superviviente`
- `Sub-Humano`
- `Humano del Amanecer`

⚔️ Zona Venenosa:
- `Humano Corrupto`
- `Humano Debilitado`
- `Humano Oscuro`
- `Humano Mutado` 

⚔️ Extras:
- `Sombra`
- `Humano Destino`
⚜️ Espectros de la Creación
🔹- - - - - - - - -💠- - - - - - - - -🔹
- La raza (⚜️) solo puede ser escogida por los elegidos del Creador.
🔹➖➖➖💠......💠➖➖➖🔹"""
start_message = """🔹➖➖💠* **Medina** *💠➖➖🔹
- Según las órdenes del Creador, mi deber es asistirte en lo que necesites. A partir de hoy estoy totalmente disponible para ti. Me encargaré de guiarte en tu viaje y ayudarte en tu recopilación de la información! 
 🔹- - - - - - - - -💠- - - - - - - - -🔹
- En caso de ser requerida, usa el comando /help y te mostraré varias opciones que puedes tomar. 
 🔹- - - - - - - - -💠- - - - - - - - -🔹
- El Creador te desea una feliz estancia!
🔹➖➖➖💠......💠➖➖➖🔹
"""
help_message = """🔹➖➖💠 * **AYUDA** * 💠➖➖🔹

 /start - Mensaje de bienvenida
 /help - Esta ayuda
 /register - Registrar jugador
 /getinfo - Estadisticas de jugador
 /razas - Mostrar razas disponibles

🔹- - - - 💠**ADMINs**💠 - - - -🔹

 /amenu - Administración
 /opmenu - Desarrollo

🔹➖➖💠 .... **FIN** .... 💠➖➖🔹"""
op_menu_message = "🛠️ Opciones de Desarrollador v1.1:\n\n" \
        "/stats - Estadísticas de uso\n" \
        "/mantenimiento - Modo mantenimiento\n" \
        "/shutdown - Apagar bot\n" \
        "/notify - Enviar notificación a todos los administradores\n" \
        "/ads - Administrar anuncios (SIN IMPLEMENTAR)\n"
admin_menu_message = """🔹➖➖➖💠 **Medina** 💠➖➖➖🔹
  |  Esto es todo por ahora:
🔹
  |
🔹 /notify - Notificar jugadores
  | 
🔹➖➖➖➖💠........💠➖➖➖➖🔹"""