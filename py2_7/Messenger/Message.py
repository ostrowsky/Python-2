from datetime import datetime
#import psycopg2
import pymysql.cursors
from db_config import conn

class Mess:

    def __init__(self, sender, text, chat):
        self.sender = sender
        self.text = str(text)
        self.time = datetime.now()
        cur = conn.cursor()
        cur.execute("""
                                                        insert into messenger.message
                                                        (sender, time, text, chatid)
                                                        values (%s, %s, %s, %s);""",
                    (
                     self.sender.id,
                     self.time,
                     self.text,
                     chat
                     ))
        conn.commit()
        conn.close()
    def __str__(self):
        return "at: {0} from: {1} received text:  {2}".format(self.time, self.sender.name, self.text)
