import telebot
import requests
import time
import threading
import datetime
import json
from functools import wraps

# Variables predefinidas
players_db = 'players.json'

with open('razas_db.json', 'r', encoding='utf-8') as file:
    razas_db = json.load(file)
    razas = ", ".join([raza['Nombre'] for raza in razas_db])

def register_command(bot, message):
    user_id = message.from_user.id

    characters = load_character_data()

    # Verificar si el usuario ya está registrado
    if any(character["ID de Usuario"] == user_id for character in characters):
        bot.send_message(user_id, "¡Ya estás registrado! Solo puedes tener un personaje.", parse_mode='Markdown')
    else:
        bot.send_message(user_id, "- Para Registrarse necesitaré su nombre y los apellidos correspondientes a sus progenitores. Sin espacios.", parse_mode='Markdown')
        bot.register_next_step_handler(message, get_character_name, bot)

# Función para obtener el nombre del personaje
def get_character_name(message, bot):
    user_id = message.from_user.id
    character_name = message.text

    if character_name:
        bot.send_message(user_id, f"- Elija su raza acorde a las características especificadas por el Creador:\n{razas}", parse_mode='Markdown')
        bot.register_next_step_handler(message, get_character_race, character_name, bot)
    else:
        bot.send_message(user_id, "El nombre del personaje no puede estar vacío. Envia un nombre válido", parse_mode='Markdown')
        bot.register_next_step_handler(message, get_character_name, bot)

# Función para obtener la raza del personaje
def get_character_race(message, character_name, bot):
    user_id = message.from_user.id
    character_race = message.text

    if character_race in razas:
        bot.send_message(user_id, "- Mencione su edad actual.", parse_mode='Markdown')
        bot.register_next_step_handler(message, get_character_age, character_name, character_race, bot)
    else:
        bot.send_message(user_id, "Elija su raza acorde a las características especificadas por el Creador", parse_mode='Markdown')
        bot.register_next_step_handler(message, get_character_race, character_name, bot)
        
# Función para obtener la edad del personaje
def get_character_age(message, character_name, character_race, bot):
    user_id = message.from_user.id
    character_age = message.text

    if character_age.isdigit():
        bot.send_message(user_id, "- Establezca el género de su paralelo.", parse_mode='Markdown')
        bot.register_next_step_handler(message, get_character_gender, character_name, character_race, character_age, bot)
    else:
        bot.send_message(user_id, "Me quieres timar? Envía un número.", parse_mode='Markdown')
        bot.register_next_step_handler(message, get_character_age, character_name, character_race, bot)

# Función para obtener el género del personaje
def get_character_gender(message, character_name, character_race, character_age, bot):
    user_id = message.from_user.id
    character_gender = message.text.lower()

    # Acepta una variedad de entradas para "masculino"
    if character_gender in ["masculino", "m", "msculino", "Masculino"]:
        character_gender = "masculino"
    # Acepta una variedad de entradas para "femenino"
    elif character_gender in ["femenino", "f", "Femenino", "fe"]:
        character_gender = "femenino"

        # Datos del personaje
        character_data = {
            "Nombre": character_name,
            "Raza": character_race,
            "Edad": character_age,
            "Género": character_gender,
            "ID de Usuario": user_id,
            "Fecha de Registro": str(datetime.datetime.now())
        }

        # Valores iniciales en el perfil
        character_data["SC"] = 0  # Vida o energía
        character_data["RANK"] = "none"
        character_data["NEXO"] = 100
        character_data["TR"] = 0
        character_data["PRIV"] = "P"

        # Guardar los datos en la base de datos (players.json)
        save_character_data(character_data, bot)

        bot.send_message(user_id, "- El registro se ha completado! Ahora tiene total libertad para andar en NeoTerra. Me retiro!")
    else:
        bot.send_message(user_id, "No se que género es ese. Solo existen dos géneros, envía uno de esos.")
        bot.register_next_step_handler(message, get_character_gender, character_name, character_race, character_age, bot)

# Función para guardar los datos del personaje en la base de datos
def save_character_data(character_data, bot):
    characters = load_character_data()
    characters.append(character_data)

    with open(players_db, 'w') as file:
        json.dump({"characters": characters}, file)

# Cargar datos de jugadores
def load_character_data():
    try:
        with open(players_db, 'r') as file:
            data = json.load(file)
            return data.get('characters', [])
    except FileNotFoundError:
        # Si el archivo no existe, retorna una lista vacía
        return []

# Registrar accion en el archivo registro.txt ubicado en la misma carpeta que este archivo
def registrar_accion(accion):
    fecha_hora_actual = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    mensaje_registro = f"{fecha_hora_actual} - {accion}\n"
    with open("registro.txt", "a") as archivo_registro:
        archivo_registro.write(mensaje_registro)