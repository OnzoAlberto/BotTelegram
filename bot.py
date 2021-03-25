import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os
import variables

PORT = int(os.environ.get('PORT', 5000))
develop = True
# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
TOKEN = variables.get_token()

# def process_code(message):
#     try:
#         chat_id = message.chat.id
#         code = message.text
#         msg = T_bot.reply_to(message, '\'Mo cerco,aspé')
#         T_bot.reply_to(message, track.from_dhl(code))
#     except Exception as e:
#         T_bot.reply_to(message, 'oooops')
#

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    print('command: ' + update.message.text + ' - from:  '+update.message.chat.first_name)
    update.message.reply_text("we " +update.message.chat.first_name +", tutt'appost?")

def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def trace(update, context):
    print('tracking from: ' + update.message.chat.first_name)
    update.message.reply_text(text='insert track number')

    dp.add_handler(MessageHandler(Filters.text, help))

    update.register_next_step_handler(update, 'process_code')
    #bot.reply_to(message, track.from_dhl())


def echo(update, context):
    """Echo the user message."""
    print('ok')
    update.message.reply_text('ok')

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():

    """Start the bot."""
    updater = Updater(TOKEN, use_context=True)
    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("trace", trace))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    if develop:
        updater.start_polling()
    else:
        updater.start_webhook(listen="0.0.0.0", port=int(PORT), url_path=TOKEN)
        updater.bot.setWebhook('https://trackbotv1.herokuapp.com/' + TOKEN)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()