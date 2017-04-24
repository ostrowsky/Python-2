import hashlib
from Message import Mess
from Chat import Chat
import psycopg2
from datetime import datetime



class User:
    users_list = []
    status_list = ('offline', 'online')
    user_statuses = {}
    def __init__(self, name, password):
        User.users_list.append(self)
        self.name = name
        self.password = str(hashlib.md5(password.encode('utf-8')))
        self.status = 'offline'
        self.contacts = []
        self.created_at = datetime.now()
        conn_string = "host='localhost' dbname='postgres' user='postgres' password='4309344'"
        conn = psycopg2.connect(conn_string)
        cur = conn.cursor()
        cur.execute("""
                        insert into messenger.user
                        (name, password, status, createdat)
                        values (%s, %s, %s, %s);""",
                    (self.name, self.password, self.status, self.created_at))

        cur.execute("""
                                select userid from messenger.user
                                where name=%s and password=%s;""",
                    (self.name, self.password))

        self.id = cur.fetchone()[0]
        conn.commit()






    def getName(self):
        return self.name


    def getStatus(self):
        return self.status


    def addContact(self, contact):
        if contact in User.users_list:
            self.contacts.append(contact)
            id = len(self.contacts)
            print("Пользователь {} добавлен в список контактов пользователя {}".format(contact.name, self.name))
            conn_string = "host='localhost' dbname='postgres' user='postgres' password='4309344'"
            conn = psycopg2.connect(conn_string)
            cur = conn.cursor()
            cur.execute("""
                                    insert into messenger.contacts
                                    (userid, contact)
                                    values (%s, %s);""",
                        (self.id, contact.id))
            conn.commit()


        else:
            print("Пользователь не зарегистрирован")


    def getContacts(self):
        if self.contacts:
            print("Список контактов пользователя {}: ".format(self.name))
            i = 1
            for contact in self.contacts:
                print("     №{} {}".format(i, contact))
                i+=1
        else:
            print("Список контактов пользователя {} пуст".format(self.name))


    def delFromContacts(self, contact):
       pass


    def connect(self):
        User.user_statuses[self.id] = User.status_list[1]

    def startChat(self, *participants):
        new_chat = Chat(self)
        new_chat.add_participants(*participants)
        if new_chat.participants:
            new_chat.printChat()
        else:
            print("Участники не добавлены")






    def receive_message(self, message):
        print("to: {0} at: {1} from: {2} received text:  {3}".format(self.name, message.time, message.sender.name, message.text))


    def __str__(self):
        return "Пользователь с ID: {0}, имя: {1}".format(self.id, self.name)
'''
    def getChat(self, contact):
        print("--------------------Чат с {}-----------------------------".format(contact.name))
        chat_with = []
        for message in Mess.messages:
            if message.recipient == self and message.sender not in chat_with:
                chat_with.append(message.sender)
            if message.sender == self and message.recipient not in chat_with:
                chat_with.append(message.recipient)


        for user in chat_with:
            if user == contact:
                for message in Mess.messages:
                    if message.recipient == user or message.sender == user:
                        if message.sender == self:
                            print(self.name, str(message.time)[:-7])
                            print("{0:<}".format(message.text))
                        if message.recipient == self:
                            concat_str = str(message.time)[:-7] + ' ' + message.sender.name
                            print("{0:>50}".format(concat_str))
                            print("{0:>50}".format(message.text))
            else:
                print("Чат с такими участниками не найден")
                print('\n')









        mess_dict = {}
        for message in Mess.messages:
            if not message.sender == self:
                mess_dict[message.sender] =  message

        print(mess_dict)
        for key, value in mess_dict.items():
            print("--------------------Чат с {}-----------------------------".format(key.name))
            if value.sender == self:
                print(self.name, str(message.time)[:-7])
                print("{0:<}".format(message.text))
            if value.recipient == self:
                concat_str = str(message.time)[:-7] + ' ' + message.sender.name
                print("{0:>50}".format(concat_str))
                print("{0:>50}".format(message.text))
'''