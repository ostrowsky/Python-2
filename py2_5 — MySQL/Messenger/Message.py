from datetime import datetime
#import psycopg2
import pymysql.cursors
class Mess:
    #messages = []

    def __init__(self, sender, text, chat):
        self.sender = sender
        self.text = str(text)
        self.time = datetime.now()
        #Mess.messages.append(self)
        conn_string = "host='localhost' dbname='postgres' user='postgres' password='4309344'"
        conn = pymysql.connect(host='localhost',
                               user='root',
                               password='4309344',
                               db='test',
                               charset='utf8mb4',
                               cursorclass=pymysql.cursors.DictCursor)
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
