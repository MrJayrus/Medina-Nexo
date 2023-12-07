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