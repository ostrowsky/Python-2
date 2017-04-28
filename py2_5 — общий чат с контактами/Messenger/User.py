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
        conn.close()






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
            conn.close()


        else:
            print("Пользователь не зарегистрирован")


    def getContacts(self):
        if self.contacts:
            conn_string = "host='localhost' dbname='postgres' user='postgres' password='4309344'"
            conn = psycopg2.connect(conn_string)
            cur = conn.cursor()
            cur.execute("""
                                            select c.contact, u.name from messenger.contacts c join messenger.user u on c.contact=u.userid
                                            where c.userid=%s;""",
                        (self.id,))

            contacts = cur.fetchall()
            conn.commit()
            conn.close()
            return contacts
        else:
            return "Список контактов пользователя {} пуст".format(self.name)


    def delFromContacts(self, contact):
       pass


    def connect(self):
        User.user_statuses[self.id] = User.status_list[1]


    def startChat(self, *participants):
        rows = self.getContacts()
        contacts = []
        for row in rows:
            contacts.append(row[0])
        new_chat = Chat(self)
        new_chat.add_participants(contacts)
        return new_chat.id



