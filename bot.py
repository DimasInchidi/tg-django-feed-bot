from telegram.ext import Updater, MessageHandler, Filters

from actions import error, reset_timer, callback_activity, callback_feeder


class Bot:
    def __init__(self, token, app_name, port):
        self._token = token
        self._app_name = app_name
        self._port = port
        self._updater = Updater(token)
        self._init_handlers()

    def run(self):
        u = self._updater
        u.start_webhook(
            # listen='0.0.0.0',
            # port=self._port,
            # url_path=self._token,

            listen='127.0.0.1',
            port=5000,
            url_path='TOKEN1'
        )
        u.bot.set_webhook(
            # 'https://{}.herokuapp.com/{}'.format(
            #     self._app_name,
            #     self._token,
            # )
            'https://4458c55b.ngrok.io/TOKEN1'
        )
        u.start_polling()
        u.idle()

    def _init_handlers(self):
        dp = self._updater.dispatcher
        self._updater.job_queue.run_repeating(
            callback_activity,
            interval=300,
            first=0.0,
            name='check_activity'
        )
        self._updater.job_queue.run_repeating(
            callback_feeder,
            interval=60,
            first=0.0,
            name='getting_feed'
        )

        dp.add_handler(MessageHandler(Filters.text, reset_timer))
        dp.add_error_handler(error)
