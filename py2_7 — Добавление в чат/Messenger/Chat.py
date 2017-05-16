import pymysql.cursors
from datetime import datetime
from Message import Mess
from db_config import *

class Chat:
    chats = []

    @classmethod
    def getChatById(cls, id):
        conn = pymysql.connect(host=HOST,
                               user=USER,
                               password=PASSWORD,
                               db=DB,
                               charset=CHARSET,
                               cursorclass=CURSORCLASS)
        cur = conn.cursor()
        cur.execute("""select owner from messenger.chat where chatid=%s;""", (str(id),))
        res = cur.fetchone()
        chat = Chat(res['owner'])
        chat.id = id
        return chat


    def __init__(self, owner):
        self.owner = owner
        self.participants = [self.owner]
        self.messages = []
        Chat.chats.append(self)
        self.created_at = datetime.now()


    def save(self):
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
                                        select MAX(chatid) from messenger.chat
                                        where owner=%s;""", (self.owner.id,))


        self.id = cur.fetchone()['MAX(chatid)']
        conn.commit()
        conn.close()

    def add_participants(self, *participants):
        for participant in [x for x in participants[0]]:
            self.participants.append(participant)


        print("Чат номер", self.id, "создан юзером", self.owner.name, "участники: ", [x.name for x in self.participants])
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
                            (self.id, part.id))
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


