import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os
import variables
import track
import telebot

PORT = int(os.environ.get('PORT', 5000))
develop = False
# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
TOKEN = variables.get_token()

T_bot = telebot.TeleBot(TOKEN)

def process_code(message):
    try:
        chat_id = message.chat.id
        code = message.text
        msg = T_bot.send_message(message, '\'Mo cerco,aspé')
        T_bot.send_message(message, track.from_dhl(code))
    except Exception as e:
        T_bot.send_message(message, 'oooops')

@T_bot.message_handler(commands=['start', 'help'])
def start(message):
    print('command: ' + message.json['text'] + ' - from: ' + message.json['from']['first_name'])
    T_bot.send_message(message.json['chat']['id'], text="we "+message.json['from']['first_name']+", tutt'appost?")
    print('**** - path : ' + str(os.path))
    if develop:
        T_bot.send_message(message.json['chat']['id'], text="Sono in locale")
    else:
        T_bot.send_message(message.json['chat']['id'], text="Sono su Eroku")

@T_bot.message_handler(commands=['trace'])
def trace(message):
    print('- from: ' + message.json['from']['first_name'])
    T_bot.send_message(message.json['chat']['id'], text='insert track number')
    T_bot.register_next_step_handler(message, process_code)


@T_bot.message_handler(func=lambda m: True)
def echo_all(message):
    print('command: ' + message.json['text'] + ' - from: ' + message.json['from']['first_name'])
    T_bot.send_message(message, "non ci sono ancora arrivato...")


def main():

    T_bot.infinity_polling(True)

    # Start the Bot
    if develop:
        T_bot.delete_webhook()
    else:
        """Start the bot."""
        updater = Updater(TOKEN, use_context=True)
        # Get the dispatcher to register handlers
        # dp = updater.dispatcher
        #
        # # on different commands - answer in Telegram
        # dp.add_handler(CommandHandler("start", start))
        # dp.add_handler(CommandHandler("help", help))
        # dp.add_handler(CommandHandler("trace", trace))
        #
        # # on noncommand i.e message - echo the message on Telegram
        # dp.add_handler(MessageHandler(Filters.text, echo_all))
        #
        # # log all errors
        # dp.add_error_handler(echo_all)

    updater.start_webhook(listen="0.0.0.0", port=int(PORT), url_path=TOKEN)
    updater.bot.setWebhook('https://trackbotv1.herokuapp.com/' + TOKEN)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
