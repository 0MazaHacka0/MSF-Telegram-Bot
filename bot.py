import config

from telegram.ext import CommandHandler, Updater

# Connect to Telegram
updater = Updater(config.TOKEN)
job_updater = updater.job_queue
dispatcher = updater.dispatcher

if __name__ == '__main__':
    # Start bot
    updater.start_polling()