import hashlib
#import psycopg2
import pymysql.cursors
from datetime import datetime
from tkinter import *
from db_config import conn
from Message import Mess
from Chat import Chat


class User:
    #users_list = []
    status_list = ('offline', 'online')
    user_statuses = {}

    @classmethod
    def getUsersList(cls):
        cur = conn.cursor()
        cur.execute("""select distinct name from messenger.user;""")
        res = cur.fetchall()
        return res


    def __init__(self, name, password):
        #User.users_list.append(self)
        self.name = name
        self.password = hashlib.md5(password.encode()).hexdigest()
        self.status = 'offline'
        self.contacts = []
        self.created_at = datetime.now()
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

        self.id = cur.fetchone()['userid']
        conn.commit()
        conn.close()








    def getName(self):
        return self.name


    def getStatus(self):
        return self.status


    def addContact(self, contact):
        if contact in User.getUsersList:
            self.contacts.append(contact)
            print("Пользователь {} добавлен в список контактов пользователя {}".format(contact.name, self.name))
            cur = conn.cursor()
            v = (self.id, contact.id)
            cur.execute("insert into messenger.contacts (userid, contact) values (%s,%s)",v)
            conn.commit()
            conn.close()


        else:
            print("Пользователь не зарегистрирован")


    def getContacts(self):
        if self.contacts:
            cur = conn.cursor()
            cur.execute("""
                                            select c.contact, u.name from messenger.contacts c join messenger.user u on c.contact=u.userid
                                            where c.userid=%s;""",
                        (self.id,))

            res = cur.fetchall()
            contacts = [(x['contact'], x['name']) for x in res]
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


