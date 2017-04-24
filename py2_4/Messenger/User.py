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
            conn_string = "host='localhost' dbname='postgres' user='postgres' password='4309344'"
            conn = psycopg2.connect(conn_string)
            cur = conn.cursor()
            cur.execute("""
                                            select name, c.contact from messenger.contacts c
                                            join messenger.user u on c.contact=u.userid
                                            where c.userid=%s;""",
                        (self.id,))

            contacts = cur.fetchall()
            conn.commit()
            return contacts
        else:
            return "Список контактов пользователя {} пуст".format(self.name)


    def delFromContacts(self, contact):
       pass


    def connect(self):
        User.user_statuses[self.id] = User.status_list[1]

    def startChat(self, *participants):
        new_chat = Chat(self)
        new_chat.add_participants(*participants)
        '''
        if new_chat.participants:
            new_chat.printChat()
        else:
            print("Участники не добавлены")
        '''
        return new_chat.id




    def receive_message(self, message):
        print("to: {0} at: {1} from: {2} received text:  {3}".format(self.name, message.time, message.sender.name, message.text))


    def __str__(self):
        return "Пользователь с ID: {0}, имя: {1}".format(self.id, self.name)
