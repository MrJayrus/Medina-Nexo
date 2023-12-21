import datetime
import json
from config import *

# Manejar el comando 
def delete_command(abot, message):
    user_id = message.from_user.id
    characters = load_character_data()
    if is_admin(user_id) or is_op(user_id):
        bot.send_message(user_id, f"💠 Como usted es desarrollador o administrador puede eliminar cualquier personaje. A continuación envíe el Nombre del Personaje que desea eliminar.", parse_mode='Markdown')
        bot.register_next_step_handler(message, ask_for_name, characters, bot)
    elif any(character["ID de Usuario"] == user_id for character in characters):
        bot.send_message(user_id, f"⚠️ PELIGRO !!!\n\nEstá a punto de eliminar su propio personaje!\n\nEnvie la palabra: (CONFIRM) para confirmar u otra para cancelar.\n\nESTA OPCIÓN NO SE PUEDE DESHACER !!!", parse_mode='Markdown')
        bot.register_next_step_handler(message, delete_user, characters, bot)
    else:
        bot.send_message(user_id, f"❌ Usted no está registrado aún!", parse_mode='Markdown')

def ask_for_name(message, characters, bot):
    user_id = message.from_user.id
    user_to_delete = message.text
    bot.send_message(user_id, f"⚠️ PELIGRO !!!\n\nEstá a punto de eliminar el personaje: {'user_to_delete'}\n\nEnvie la palabra: (CONFIRM) para confirmar u otra para cancelar.\n\nESTA OPCIÓN NO SE PUEDE DESHACER !!!", parse_mode='Markdown')
    bot.register_next_step_handler(message, delete_user_op, characters, user_to_delete, bot)

def delete_user_op(message, characters, user_to_delete, bot):
    user_id = message.from_user.id
    deleted_user = user_to_delete
    if message.text == "CONFIRM":
        bot.send_message(user_id, f"⚙️ DESARROLLADOR\n\n{'deleted_user'}", parse_mode='Markdown')
        for character in characters:
            if character["Nombre"] == user_to_delete:
                # Remover personaje de la base de datos
                characters.remove(character)
                # Actualiza los datos de personajes en el archivo JSON
                save_character_data(characters)
                # Envía un mensaje de confirmación al usuario
                bot.send_message(user_id, f"💠 Personaje {'deleted_user'} eliminado con éxito!", parse_mode='Markdown')
                break
    else:
        bot.send_message(user_id, f"❌ El personaje no se eliminó!", parse_mode='Markdown')

def delete_user(message, characters, bot):
    user_id = message.from_user.id
    if message.text == "CONFIRM":
        for character in characters:
            if character["ID de Usuario"] == user_id:
                bot.send_message(user_id, f"💠 Personaje {character['Nombre']} eliminado con éxito!", parse_mode='Markdown')
    else:
        bot.send_message(user_id, f"❌ Error al eliminar el personaje!\n\nSi usted cree que es un error póngase en contacto con @MrJayrus para solucionarlo.", parse_mode='Markdown')
