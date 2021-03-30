import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os
import variables
import track
#from pyTelegramBotAPI
import telebot
from flask import Flask, request

TOKEN = variables.get_token()
bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)


def process_code(message):
    try:
        chat_id = message.chat.id
        code = message.text
        msg = bot.send_message(message, '\'Mo cerco,aspé')
        bot.send_message(message, track.from_dhl(code))
    except Exception as e:
        bot.send_message(message, 'oooops')


@bot.message_handler(commands=['start', 'help'])
def start(message):
    print('command: ' + message.json['text'] + ' - from: ' + message.json['from']['first_name'])
    bot.send_message(message.json['chat']['id'], text="we "+message.json['from']['first_name']+", tutt'appost?")
    print('path : ' + str(os.path))

@bot.message_handler(commands=['trace'])
def trace(message):
    print('- from: ' + message.json['from']['first_name'])
    bot.send_message(message.json['chat']['id'], text='insert track number')
    bot.register_next_step_handler(message, process_code)


@bot.message_handler(func=lambda m: True)
def echo_all(message):
    print('command: ' + message.json['text'] + ' - from: ' + message.json['from']['first_name'])
    bot.send_message(message, "non ci sono ancora arrivato...")

@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://trackbotv1.herokuapp.com/' + TOKEN)
    return "!", 200


while(True):
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
