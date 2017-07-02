import logging
from datetime import datetime
from database import Database


def reset_timer(bot, update):
    if str(update.message.chat_id) == '-1001146340312':
        db = Database()
        db.set_last_activity()
        logging.info("Time reseted")
    else:
        logging.info("Bot getting post from user, but its not our user: %s", update.message.chat_id)


def callback_feeder(bot, job):
    db = Database()
    db.update_post()
    logging.info("Bot already reload new feed to db")


def callback_activity(bot, update):
    db = Database()
    timerstamp = db.get_last_activity()
    logging.info("last activity is %s", timerstamp)
    if timerstamp == 0 or timerstamp < datetime.now().timestamp() - 600:
        feed = db.get_posts()
        logging.info("newest feed is %s", feed)
        if len(feed) > 0:
            message = ""
            jobs = ">> Jobs"
            blogs = ">> Blogs"
            links = ">> Links"
            for i in feed:
                if i[3] == 'link':
                    links += '\n- <a href="' + i[2] + '">' + i[1] + '</a>'
                if i[3] == 'blog':
                    blogs += '\n- <a href="' + i[2] + '">' + i[1] + '</a>'
                if i[3] == 'job':
                    jobs += '\n- <a href="' + i[2] + '">' + i[1] + '</a>'
            if jobs != ">> Jobs":
                message += jobs + '\n\n'
            if blogs != ">> Blogs":
                message += blogs + '\n\n'
            if links != ">> Links":
                message += links + '\n\n'
            bot.sendMessage(chat_id='-1001146340312', text=message, parse_mode='HTML', disable_web_page_preview=True)
            db.set_last_posts()
        else:
            logging.info("user not active, but no new unsend feed")
    else:
        logging.info("user still have conversation")


def error(bot, update, error):
    logging.warning('Update "%s" caused error "%s"' % (update, error))
