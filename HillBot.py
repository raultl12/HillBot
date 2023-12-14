from codificador import CodificadorHill
import numpy as np
import telebot
from access import token

user_name = 'hill_encoder_bot'

bot = telebot.TeleBot(token)
codificador = CodificadorHill(3)
codificador.clave = np.array([
    [1, 1, 0],
    [1, 0, 1],
    [0, 1, 0]
])

estado_bot = {
    "apagado": 0,
    "encendido": 1,
}

estado_codificacion = {
    "codificando": 1,
    "decodificando": 2
}

current_state = estado_bot["apagado"]
current_state_codificacion = estado_codificacion["codificando"]

# Comandos
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, 'Bienvenido al bot de cifrado Hill')

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, 'Envia un mensaje para cifrarlo')

# Comando /on para encender el bot
@bot.message_handler(commands=['on'])
def on(message):
    global current_state
    global current_state_codificacion
    current_state = estado_bot["encendido"]
    current_state_codificacion = estado_codificacion["codificando"]

    bot.reply_to(message, "Bot encendido en modo codificacion, usa el comando /off para apagarlo")

# Comando /off para apagar el bot
@bot.message_handler(commands=['off'])
def off(message):
    global current_state
    current_state = estado_bot["apagado"]

    bot.reply_to(message, "Bot apagado, usa el comando /on para encenderlo")


@bot.message_handler(commands=['encrypt'])
def encrypt(message):
    # Si el bot esta apagado, informar al usuario
    if current_state == estado_bot["apagado"]:
        bot.reply_to(message, "El bot esta apagado, usa el comando /on para encenderlo")
        return
    global current_state_codificacion
    current_state_codificacion = estado_codificacion["codificando"]
    
    bot.reply_to(message, "Cambiado a modo codificacion")

# Comando /decode para decodificar el texto
@bot.message_handler(commands=['decrypt'])
def decrypt(message):
    # Si el bot esta apagado, informar al usuario
    if current_state == estado_bot["apagado"]:
        bot.reply_to(message, "El bot esta apagado, usa el comando /on para encenderlo")
        return
    global current_state_codificacion
    current_state_codificacion = estado_codificacion["decodificando"]

    bot.reply_to(message, "Cambiado a modo decodificacion")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    # Si esta encendido y codificando, codifica el mensaje
    if current_state == estado_bot["encendido"] and current_state_codificacion == estado_codificacion["codificando"]:
        try:
            textoCifrado = codificador.Cifrar(message.text)
        except:
            textoCifrado = "Error al cifrar el mensaje"
        
        bot.reply_to(message, textoCifrado)
    
    # Si esta encendido y decodificando, decodifica el mensaje
    elif current_state == estado_bot["encendido"] and current_state_codificacion == estado_codificacion["decodificando"]:
        try:
            textoDescifrado = codificador.Descifrar(message.text)
        except:
            textoDescifrado = "Error al descifrar el mensaje"
            
        bot.reply_to(message, textoDescifrado)

if __name__ == '__main__':
    bot.polling(non_stop=True)