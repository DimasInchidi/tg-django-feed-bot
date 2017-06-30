import logging
import os

import psycopg2
from datetime import datetime

from rss import NewFeed


class Database:
    def __init__(self):
        self._con = psycopg2.connect(host=os.environ.get("DB_HOST"),
                                     user=os.environ.get("DB_USER"),
                                     password=os.environ.get("DB_PASS"),
                                     database=os.environ.get("DB_NAME"),
                                     port=5432, sslmode='require')

    def set_last_activity(self):
        con = self._con
        cur = con.cursor()
        time_val = float(datetime.now().timestamp())
        cur.execute("UPDATE last_update SET time = %s", (time_val,))
        con.commit()

    def get_last_activity(self):
        con = self._con
        cur = con.cursor()
        cur.execute("SELECT time FROM last_update WHERE feed_id = 1")
        return cur.fetchone()[0]

    def set_last_reload(self):
        con = self._con
        cur = con.cursor()
        time_val = float(datetime.now().timestamp())
        cur.execute("UPDATE last_reload SET time = %s", (time_val,))
        con.commit()

    def get_last_reload(self):
        con = self._con
        cur = con.cursor()
        cur.execute("SELECT time FROM last_reload WHERE reload_id = 1")
        return cur.fetchone()[0]

    def set_last_posts(self):
        con = self._con
        cur = con.cursor()
        time_val = float(datetime.now().timestamp())
        cur.execute("UPDATE posts SET publish_time = %s WHERE publish_time = 0", (time_val,))
        con.commit()

    def get_last_posts(self):
        con = self._con
        cur = con.cursor()
        cur.execute("SELECT * FROM posts WHERE publish_time = 0")
        return cur.fetchall()

    def update_post(self):
        start_from = self.get_last_reload()
        con = self._con
        cur = con.cursor()
        logging.info("Getting feed from %s", start_from)
        feed = NewFeed().get_news(start_from)
        logging.info("The new feed >> %s", feed)
        cur.executemany(
            "INSERT INTO posts (title, link, post_type, post_time) VALUES (%s,%s,%s,%s)",
            feed
        )
        con.commit()
        self.set_last_reload()

    def get_posts(self):
        result = self.get_last_posts()
        return result

    def __del__(self):
        db = self._con
        db.cursor().close()
        db.close()
