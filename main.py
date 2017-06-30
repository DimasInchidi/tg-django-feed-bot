import os
import logging
from bot import Bot

if __name__ == '__main__':
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

    token = os.environ.get("TOKEN")
    app_name = os.environ.get("APP_NAME")
    port = int(os.environ.get('PORT', '5000'))

    logging.warning('Starting...')

    bot = Bot(token, app_name, port)
    bot.run()
