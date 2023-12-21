import json
import telebot
import time
import datetime

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

# Registrar accion en el archivo registro.txt ubicado en la msma carpeta que este archivo
def registrar_accion(accion):
    fecha_hora_actual = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    mensaje_registro = f"{fecha_hora_actual} - {accion}\n"
    with open("registro.txt", "a", encoding='utf-8') as archivo_registro:
        archivo_registro.write(mensaje_registro)

# Función para verificar si un usuario es administrador
def is_admin(user_id):
    return user_id in administrador

# Función para verificar si un usuario es desarrollador
def is_op(user_id):
    return user_id in operador

# Función para guardar los datos del personaje en la base de datos
def save_character_data(character_data):
    characters = load_character_data()
    characters.append(character_data)

    with open(players_db, 'w') as file:
        json.dump({"characters": characters}, file)

def load_character_data():
    try:
        with open(players_db, 'r') as file:
            data = json.load(file)
            return data.get('characters', [])
    except (FileNotFoundError, json.JSONDecodeError):
        return []

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
 /delete - Eliminar un personaje

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