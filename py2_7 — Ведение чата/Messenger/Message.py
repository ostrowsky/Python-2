from datetime import datetime
#import psycopg2
import pymysql.cursors
from db_config import *


class Mess:
    @classmethod
    def getMessagesByChat(cls, chatid):
        messages = []
        conn = pymysql.connect(host=HOST,
                               user=USER,
                               password=PASSWORD,
                               db=DB,
                               charset=CHARSET,
                               cursorclass=CURSORCLASS)
        cur = conn.cursor()
        cur.execute("""select messageid, sender, text from messenger.message
                    where chatid=%s;""", (chatid,))
        res = cur.fetchall()
        for message in res:
            new_message = Mess(message['sender'], message['text'], chatid )
            new_message.id = message['messageid']
            messages.append(new_message)
        return messages


    def __init__(self, sender, text, chat):
        self.sender = sender
        self.text = str(text)
        self.time = datetime.now()
        self.chatid = chat


    def save(self):
        conn = pymysql.connect(host=HOST,
                               user=USER,
                               password=PASSWORD,
                               db=DB,
                               charset=CHARSET,
                               cursorclass=CURSORCLASS)
        cur = conn.cursor()
        cur.execute("""
                                                        insert into messenger.message
                                                        (sender, time, text, chatid)
                                                        values (%s, %s, %s, %s);""",
                    (
                     self.sender.id,
                     self.time,
                     self.text,
                     self.chatid
                     ))
        cur.execute("""
                                        select messageid from messenger.message
                                        where sender=%s and time=%s and text=%s and chatid=%s;""",
                    (self.sender.id,
                     self.time,
                     self.text,
                     self.chatid,))
        self.id = cur.fetchone()['messageid']
        conn.commit()
        conn.close()


    def __str__(self):
        return "at: {0} from: {1} received text:  {2}".format(self.time, self.sender.name, self.text)
