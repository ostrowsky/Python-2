from datetime import datetime
import psycopg2

class Mess:
    #messages = []

    def __init__(self, sender, text, chat):
        if Mess.messages:
            self.id = Mess.messages[-1].id + 1
        else:
            self.id = 1
        self.sender = sender
        self.text = str(text)
        self.time = datetime.now()
        #Mess.messages.append(self)
        conn_string = "host='localhost' dbname='postgres' user='postgres' password='4309344'"
        conn = psycopg2.connect(conn_string)
        cur = conn.cursor()
        cur.execute("""
                                                        insert into messenger.message
                                                        (messageid, sender, time, text, chatid)
                                                        values (%s, %s, %s, %s, %s);""",
                    (
                    self.id,
                     self.sender.id,
                     self.time,
                     self.text,
                     chat
                     ))
        conn.commit()
    def __str__(self):
        return "to: {0} at: {1} from: {2} received text:  {3}".format(self.recipient, self.time, self.sender.name, self.text)
