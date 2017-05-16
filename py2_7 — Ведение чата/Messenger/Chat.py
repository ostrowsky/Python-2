import pymysql.cursors
from datetime import datetime
from Message import Mess
from db_config import *

class Chat:
    chats = []

    @classmethod
    def getChatById(cls, chat_id):
        conn = pymysql.connect(host=HOST,
                               user=USER,
                               password=PASSWORD,
                               db=DB,
                               charset=CHARSET,
                               cursorclass=CURSORCLASS)
        cur = conn.cursor()
        cur.execute("""select owner from messenger.chat where chatid=%s;""", (str(chat_id),))
        res = cur.fetchone()
        chat = Chat(res['owner'])
        chat.id = chat_id
        return chat

    @classmethod
    def getChatByParticipants(cls, owner, participant):
        conn = pymysql.connect(host=HOST,
                               user=USER,
                               password=PASSWORD,
                               db=DB,
                               charset=CHARSET,
                               cursorclass=CURSORCLASS)
        cur = conn.cursor()
        cur.execute("""select c.owner, c.chatid, cp1.chatid, cp1.participant, cp2.participant from messenger.chat c
                    join messenger.chat_participants cp1 on c.chatid = cp1.chatid
                    join messenger.chat_participants cp2 on cp1.chatid = cp2.chatid
                    where %s = cp1.participant and %s = cp2.participant;""", (owner.id, participant.id))
        res = cur.fetchall()
        if res:
            chat = Chat(owner)
            chat.id = int(res[0]['chatid'])
            chat.owner = owner
            chat.participants = [res[0]['participant'], res[0]['cp2.participant']]
            chat.messages = Mess.getMessagesByChat(chat.id)
        else:
            chat = None
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
            message.save()
            self.messages.append(message)
            return message
        else:
            print("Пользователь {} не является участником чата {}".format(sender.name, self.id))


    def __str__(self):
        return "Чат номер {} пользователя {} с пользователями {}".format(self.id, self.owner.name, [x for x in self.participants])


