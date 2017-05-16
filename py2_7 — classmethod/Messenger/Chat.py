import pymysql.cursors
from datetime import datetime
from Message import Mess
from db_config import *

class Chat:
    chats = []
    def __init__(self, owner):

        self.owner = owner
        self.participants = [self.owner.id]
        self.messages = []
        Chat.chats.append(self)
        self.created_at = datetime.now()
        conn = pymysql.connect(host=HOST,
                               user=USER,
                               password=PASSWORD,
                               db=DB,
                               charset=CHARSET,
                               cursorclass=CURSORCLASS)
        cur = conn.cursor()
        cur.execute("""
                                insert into messenger.chat
                                (owner, createdat)
                                values (%s, %s);""",
                    (self.owner.id, self.created_at))
        cur.execute("""
                                        select chatid, MAX(createdat) from messenger.chat
                                        GROUP BY chatid;""")


        self.id = cur.fetchone()['chatid']
        conn.commit()
        conn.close()

    def add_participants(self, *participants):
        for participant in [x for x in participants[0]]:
            if participant in [x.id for x in self.owner.contacts] and participant not in self.participants:
                self.participants.append(participant)
            else:
                print("Пользователь {} не найден в списке контактов пользователя {}".format(participant,
                                                                                            self.owner.name))

        print("Чат номер", self.id, "создан юзером", self.owner.name, "участники: ", self.participants)
        for part in self.participants:
            conn = pymysql.connect(host=HOST,
                                   user=USER,
                                   password=PASSWORD,
                                   db=DB,
                                   charset=CHARSET,
                                   cursorclass=CURSORCLASS)
            cur = conn.cursor()
            cur.execute("""
                                                                insert into messenger.chat_participants
                                                                (chatid, participant)
                                                                values (%s, %s);""",
                            (self.id, part))
            conn.commit()
            conn.close()


    def addMessage(self, sender, text):
        if sender.id in self.participants or sender == self.owner:
            message = Mess(sender, text, self.id)
            self.messages.append(message)
            return message
        else:
            print("Пользователь {} не является участником чата {}".format(sender.name, self.id))


    def __str__(self):
        return "Чат пользователя {} с пользователями {}".format(self.owner.name, [x for x in self.participants])


