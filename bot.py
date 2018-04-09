import config
from telegram.ext import CommandHandler, Updater
import logging

import msf_helper as msf
from SQLighter import SQLighter

# Connect to Telegram
updater = Updater(config.TOKEN)

# Configure Telegram Bot
job_updater = updater.job_queue
dispatcher = updater.dispatcher

# Read chat_id's from DB
db = SQLighter('db.sqlite')
user_ids = set()

# Logger
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

new_sessions = list()


def help(bot, update):
    update.message.reply_text('''
/sessions - показать доступные сессии
/jobs - показать запущенные задачи
/subscribe - подписаться на обновления
/unsubscribe - отписаться от обновлений
/ids - показать все id в базе
/id - id твоего сообщения
    ''')


# Update user_ids variable
def updateUserIDs():
    global user_ids, db
    temp = db.get_users()
    new_list = list()
    for i in temp:
        new_list.append(i[1])
    user_ids = new_list


# Send message with available sessions
def sessions(bot, update):
    for id, session in msf.getHumanSessionList().items():
        print(session)
        bot.send_message(chat_id=update.message.chat.id, text=session)
    if len(msf.getHumanSessionList()) == 0:
        bot.send_message(chat_id=update.message.chat.id, text='There are no sessions')


def jobs(bot, update):
    jobs = msf.getHumanJobsList()
    if jobs:
        for job in jobs:
            bot.send_message(chat_id=update.message.chat.id, text=job)


def sessions_callback(bot, job):
    global new_sessions
    sessions = msf.getHumanSessionList()
    for user_id in user_ids:
        if sessions:
            for session_id in set(new_sessions):
                if session_id in sessions:
                    bot.send_message(chat_id=user_id, text=sessions[session_id])
    new_sessions = list()


# Callback send message with new sessions
def alarmNewSession_callback(bot, job):
    temp = msf.getNewSessions()
    if temp:
        for user_id in user_ids:
            print(user_ids)
            for session in temp:
                print(user_id)
                bot.send_message(chat_id=user_id, text=temp[session])
                new_sessions.append(session)
        job_updater.run_once(sessions_callback, 10)


# Subscribe user
def subscribe(bot, update):
    state = db.add_user(update.message.chat.id)
    updateUserIDs()
    if state is False:
        bot.send_message(chat_id=update.message.chat.id, text='You already subscribed')
    else:
        bot.send_message(chat_id=update.message.chat.id, text='You have successfully subscribed')


# Unsubscribe user
def unsubscribe(bot, update):
    state = db.delete_user(update.message.chat.id)
    updateUserIDs()
    if state is False:
        bot.send_message(chat_id=update.message.chat.id, text='You are not subscribed')
    else:
        bot.send_message(chat_id=update.message.chat.id, text='You have successfully unsubscribed')


# Show all IDs in DB
def ids(bot, update):
    for i in user_ids:
        bot.send_message(chat_id=update.message.chat.id, text=str(i))


# Show current message id
def id(bot, update):
    bot.send_message(chat_id=update.message.chat.id, text=update.message.chat.id)


# Job queue
job_updater.run_repeating(alarmNewSession_callback, interval=1, first=0)

# Handlers
dispatcher.add_handler(CommandHandler('start', help))
dispatcher.add_handler(CommandHandler('help', help))
dispatcher.add_handler(CommandHandler('sessions', sessions))
dispatcher.add_handler(CommandHandler('jobs', jobs))
dispatcher.add_handler(CommandHandler('subscribe', subscribe))
dispatcher.add_handler(CommandHandler('unsubscribe', unsubscribe))
dispatcher.add_handler(CommandHandler('ids', ids))
dispatcher.add_handler(CommandHandler('id', id))

if __name__ == '__main__':
    updateUserIDs()
    updater.start_polling()
