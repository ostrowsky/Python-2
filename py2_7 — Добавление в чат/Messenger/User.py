import hashlib
from Message import Mess
from Chat import Chat
#import psycopg2
import pymysql.cursors
from datetime import datetime
from tkinter import *
from db_config import *


class User:
    status_list = ('offline', 'online')


    @classmethod
    def getUsersList(cls):
        conn = pymysql.connect(host=HOST,
                               user=USER,
                               password=PASSWORD,
                               db=DB,
                               charset=CHARSET,
                               cursorclass=CURSORCLASS)
        cur = conn.cursor()
        cur.execute("""select distinct userid, name, password from messenger.user;""")
        res = cur.fetchall()
        return res


    @classmethod
    def getUserById(cls, id):
        conn = pymysql.connect(host=HOST,
                               user=USER,
                               password=PASSWORD,
                               db=DB,
                               charset=CHARSET,
                               cursorclass=CURSORCLASS)
        cur = conn.cursor()
        cur.execute("""select name, password from messenger.user where userid=%s;""",(str(id),))
        res = cur.fetchone()
        user = User(res['name'], res['password'])
        user.id = id
        return user

    def __init__(self, name, password):
        self.name = name
        self.password = hashlib.md5(password.encode()).hexdigest()
        self.status = 'offline'
        self.contacts = []
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




    def getStatus(self):
        return self.status


    def addContact(self, contact):
        res = False
        try:
            if int(contact) not in [x['userid'] for x in User.getUsersList()]:
                res = "Пользователь с номером {} не зарегистрирован\n".format(contact)
            else:
                for user in User.getUsersList():
                    if int(contact) == user['userid'] and (not self.getContacts() or int(contact) not in [x[1] for x in self.getContacts()]):
                        self.contacts.append(user)
                        conn = pymysql.connect(host=HOST,
                               user=USER,
                               password=PASSWORD,
                               db=DB,
                               charset=CHARSET,
                               cursorclass=CURSORCLASS)
                        cur = conn.cursor()
                        new_contact = (self.id, contact)
                        cur.execute("insert into messenger.contacts (userid, contact) values (%s,%s)",new_contact)
                        conn.commit()
                        conn.close()
                        res = "Пользователь {} добавлен в список контактов пользователя {}".format(user['name'], self.name)
                    elif int(contact) == user['userid'] and int(contact) in [x[1] for x in self.getContacts()]:
                        res = "Пользователь {} уже добавлен в список контактов пользователя {}".format(user['name'], self.name)
        except ValueError:
            res = 'Введите числовой ID пользователя'

        return res


    def getContacts(self):
        conn = pymysql.connect(host=HOST,
                               user=USER,
                               password=PASSWORD,
                               db=DB,
                               charset=CHARSET,
                               cursorclass=CURSORCLASS)
        cur = conn.cursor()
        cur.execute("""
                                            select distinct c.userid, c.contact, u.name from messenger.contacts c join messenger.user u on c.contact=u.userid
                                            where c.userid=%s;""",
                        (self.id,))

        res = cur.fetchall()
        if res:
            contacts = [(x['userid'], x['contact'], x['name']) for x in res]
        else:
            contacts = None
        conn.commit()
        conn.close()
        return contacts

    def delFromContacts(self, contact):
       pass



    def startChat(self, *participants):
        contacts = [x for x in participants]
        new_chat = Chat(self)
        new_chat.save()
        new_chat.add_participants(contacts)
        return new_chat.id


