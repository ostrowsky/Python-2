from Message import Mess
import psycopg2

class Chat:
    chats = []
    def __init__(self, owner):

        self.owner = owner
        self.participants = [self.owner]
        self.messages = []
        Chat.chats.append(self)
        self.id = len(Chat.chats)
        conn_string = "host='localhost' dbname='postgres' user='postgres' password='4309344'"
        conn = psycopg2.connect(conn_string)
        cur = conn.cursor()
        cur.execute("""
                                insert into messenger.chat
                                (chatid, owner)
                                values (%s, %s);""",
                    (self.id, self.owner.id))
        conn.commit()

    def add_participants(self, *participants):
        for participant in participants:
            if participant in self.owner.contacts:
                self.participants.append(participant)
                conn_string = "host='localhost' dbname='postgres' user='postgres' password='4309344'"
                conn = psycopg2.connect(conn_string)
                cur = conn.cursor()
                cur.execute("""
                                                                insert into messenger.chat_participants
                                                                (chat_id, participant)
                                                                values (%s, %s);""",
                            (self.id, participant.id))
                conn.commit()

            else:
                print("Пользователь {} не найден в списке контактов пользователя {}".format(participant.name,
                                                                                            self.owner.name))




    def addMessage(self, sender, text):
        if sender in self.participants or sender == self.owner:
            message = Mess(sender, text, self.id)
            self.messages.append(message)
            return True
        else:
            print("Пользователь {} не является участником чата".format(sender.name))

    def printChat(self):

        print("--------------------Чат с {}-----------------------------".format([x.name for x in self.participants]))

        while True:
            for message in self.messages:
                if message.sender == self.owner:
                    print(self.owner.name, str(message.time)[:-7])
                    print("{0:<}".format(message.text))
                else:
                    concat_str = str(message.time)[:-7] + ' ' + message.sender.name
                    print("{0:>50}".format(concat_str))
                    print("{0:>50}".format(message.text))
            curr_participant = int(input(
                "Введите номер участника: {} для {}\n".format([x for x in range(len(self.participants))],
                                                              [x.name for x in self.participants])))
            new_message = input("Введите сообщение от имени {} или X для выхода из чата\n".format(
                self.participants[curr_participant].name))
            if new_message != 'X':
                self.addMessage(self.participants[curr_participant], new_message)
            else:
                break




    def __str__(self):
        return "Чат пользователя {} с пользователями {}".format(self.owner.name, [x.name for x in self.participants])