#import psycopg2
import pymysql.cursors
from datetime import datetime
from db_config import conn
from Message import Mess

class Chat:
    chats = []
    conn_string = "host='localhost' dbname='postgres' user='postgres' password='4309344'"
    def __init__(self, owner):

        self.owner = owner
        self.participants = [self.owner.id]
        self.messages = []
        Chat.chats.append(self)
        self.created_at = datetime.now()
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
            conn = pymysql.connect(host='localhost',
                                   user='root',
                                   password='4309344',
                                   db='test',
                                   charset='utf8mb4',
                                   cursorclass=pymysql.cursors.DictCursor)
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



'''
    def printChat(self):

        print("--------------------Чат с {}-----------------------------".format([x.name for x in self.participants]))

        while True:
            curr_participant = int(input(
                "Введите номер участника: {} для {}\n".format([x for x in range(len(self.participants))],
                                                              [x.name for x in self.participants])))
            new_message = input("Введите сообщение от имени {} или X для выхода из чата\n".format(
                self.participants[curr_participant].name))
            if new_message != 'X':
                self.addMessage(self.participants[curr_participant], new_message)
            else:
                break
            conn = psycopg2.connect(Chat.conn_string)
            cur = conn.cursor()
            cur.execute("""select m.*, u.name from messenger.message m join messenger.user u on m.sender=u.userid where chatid=%s order by time;""",(self.id,))
            messages = cur.fetchall()
            conn.commit()
            conn.close()

            for message in messages:
                sender = message[1]
                time = message[2]
                text = message[3]
                name = message[-1]
                if sender == self.owner.id:
                    print(self.owner.name, str(time)[:-7])
                    print("{0:<}".format(text))
                else:
                    concat_str = str(time)[:-7] + ' ' + name
                    print("{0:>50}".format(concat_str))
                    print("{0:>50}".format(text))
'''




