from codificador import CodificadorHill
import numpy as np
import telebot
from access import token

user_name = 'hill_encoder_bot'

bot = telebot.TeleBot(token)
codificador = CodificadorHill(3)
codificador.clave = np.array([
    [35, 53, 12],
    [12, 21, 5],
    [2, 4, 1]
])

# Comandos
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, 'Bienvenido al bot de cifrado Hill')

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, 'Envia un mensaje para cifrarlo')

@bot.message_handler(commands=['encrypt'])
def encrypt(message):
    if message.chat.type == "supergroup":
        txt = message.text[len(f'/encrypt@{user_name} '):]
    else:
        txt = message.text[len('/encrypt '):]
    
    textoCifrado = codificador.Cifrar(txt)
    bot.reply_to(message, textoCifrado)

# Comando /decode para decodificar el texto
@bot.message_handler(commands=['decrypt'])
def decrypt(message):
    if message.chat.type == "supergroup":
        txt = message.text[len(f'/decrypt@{user_name} '):]
    else:
        txt = message.text[len('/decrypt '):]

    textoDescifrado = codificador.Descifrar(txt)
    bot.reply_to(message, textoDescifrado)


if __name__ == '__main__':
    bot.polling(non_stop=True)