from telegram.ext import updater
import track, keys
import telebot
T_bot = telebot.TeleBot(keys.get_token())

def a():
    return track.func_1()

def process_code(message):
    try:
        chat_id = message.chat.id
        code = message.text
        msg = T_bot.reply_to(message, '\'Mo cerco,aspé')
        T_bot.reply_to(message, track.from_dhl(code))
    except Exception as e:
        T_bot.reply_to(message, 'oooops')

@T_bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    print('command: ' + message.json['text'] + ' - from: ' + message.json['from']['first_name'])
    T_bot.reply_to(message, "we "+message.json['from']['first_name']+", tutt'appost?")

@T_bot.message_handler(commands=['dhl'])
def find_order(message):
    print('- from: ' + message.json['from']['first_name'])
    T_bot.send_message(message.json['chat']['id'], text='insert track number')
    T_bot.register_next_step_handler(message, process_code)
    #bot.reply_to(message, track.from_dhl())


@T_bot.message_handler(commands=['vaccini'])
def send_vaccini(message):
    print('Vaccini request from: ' + message.json['from']['first_name'])
    # I take the data from the official website
    region_list = track.download_from_url()
    for region in region_list:
        T_bot.reply_to(message, 'Regione: ' + region['nome_area'] + '\n' + 'Dosi somministrate: ' + str(region['dosi_somministrate']) + '\n')


@T_bot.message_handler(func=lambda m: True)
def echo_all(message):
    print('command: ' + message.json['text'] + ' - from: ' + message.json['from']['first_name'])
    T_bot.reply_to(message, "non ci sono ancora arrivato...")


T_bot.poll()

#updater.bot.setWebhook('https://trackbotv1.herokuapp.com/' + keys.get_token())

#infinity_polling(True)