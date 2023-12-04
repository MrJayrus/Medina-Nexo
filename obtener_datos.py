import telebot
import requests
import time
import threading
import datetime
import json
from functools import wraps

# Variables predefinidas
players_db = 'players.json'
# Cargar base de datos de ids de usuarios local
with open('ids.json', 'r') as file:
    data = json.load(file)
administrador = data['admins']

# Función para verificar si un usuario es administrador
def is_admin(user_id):
    return user_id in administrador

# Registrar accion en el archivo registro.txt ubicado en la msma carpeta que este archivo
def registrar_accion(accion):
    fecha_hora_actual = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    mensaje_registro = f"{fecha_hora_actual} - {accion}\n"
    with open("registro.txt", "a") as archivo_registro:
        archivo_registro.write(mensaje_registro)

# Cargar datos de jugadores
def load_character_data():
    try:
        with open(players_db, 'r') as file:
            data = json.load(file)
            return data.get('characters', [])
    except FileNotFoundError:
        # Si el archivo no existe, retorna una lista vacía
        return []

def get_user_info_command(bot, message):
    user_id = message.from_user.id
    try:
        user_to_lookup = message.text.split(" ")[1]
    except IndexError:
        bot.reply_to(message, "Para darte la informacion que quieres debes usar el comando asi: /getinfo MrJayrus")
        return

    # Cargar los datos de los personajes desde la base de datos
    characters = load_character_data()

    if is_admin(user_id):
        # Administradores pueden acceder a la información de cualquier usuario
        user_found = False
        for character in characters:
            if character["Nombre"] == user_to_lookup:
                user_info = f"Nombre: {character['Nombre']}\n" \
                            f"Raza: {character['Raza']}\n" \
                            f"Edad: {character['Edad']}\n" \
                            f"Género: {character['Género']}\n" \
                            f"Registro: {character['Fecha de Registro']}\n" \
                            f"SC: {character['SC']}\n" \
                            f"Rank: {character['RANK']}\n" \
                            f"Nexo: {character['NEXO']}\n" \
                            f"TR: {character['TR']}\n" \
                            f"Priv: {character['PRIV']}"
                bot.reply_to(message, user_info)
                user_found = True
                registrar_accion(f"El usuario: {user_id} buscó el personaje: {user_to_lookup}")
                break

        if not user_found:
            bot.reply_to(message, "No encontré ese suario. Verifica el nombre del usuario e intentalo de nuevo.")
    else:
        # Usuarios normales solo pueden acceder a su propia información
        user_found = False
        for character in characters:
            if character["Nombre"] == user_to_lookup and character["ID de Usuario"] == user_id:
                user_info = f"Nombre: {character['Nombre']}\n" \
                            f"Raza: {character['Raza']}\n" \
                            f"Edad: {character['Edad']}\n" \
                            f"Género: {character['Género']}\n" \
                            f"Registro: {character['Fecha de Registro']}\n" \
                            f"SC: {character['SC']}\n" \
                            f"Rank: {character['RANK']}\n" \
                            f"Nexo: {character['NEXO']}\n" \
                            f"TR: {character['TR']}\n" \
                            f"Priv: {character['PRIV']}"
                bot.reply_to(message, user_info)
                user_found = True
                registrar_accion(f"El usuario: {user_id} buscó el personaje: {user_to_lookup}")
                break

        if not user_found:
            bot.reply_to(message, "No tienes permiso para ver su información!")
            registrar_accion(f"El usuario: {user_id} trató de buscar el personaje: {user_to_lookup}")