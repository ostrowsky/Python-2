from User import User
from Message import Mess
from Chat import Chat
import psycopg2

'''
В данной версии реализуется базовый функционал приложения Messenger
(без реализации сетевого взаимодействия)
по созданию объектно-ориентированной модели пользователей и сообщений,
добавлению пользователей к списку контактов,
отправке сообщений и отображения их истории

20.04.17 - Добавлено взаимодействие с СУБД PostgreSQL
'''
conn_string = "host='localhost' dbname='postgres' user='postgres' password='4309344'"
conn = psycopg2.connect(conn_string)
cur = conn.cursor()
cur.execute("""
        DROP TABLE IF EXISTS messenger.user
        DROP TABLE IF EXISTS messenger.chat
        DROP TABLE IF EXISTS messenger.message
        DROP TABLE IF EXISTS messenger.chat_participants
        DROP TABLE IF EXISTS messenger.contacts

        CREATE TABLE IF NOT EXISTS messenger.user (userid integer PRIMARY KEY DEFAULT nextval('serial'), name varchar(45), password varchar(256), status varchar(45))
        CREATE TABLE IF NOT EXISTS messenger.chat (chatid integer PRIMARY KEY DEFAULT nextval('serial'), owner integer) WHERE table_constraint is: FOREIGN KEY owner REFERENCES user (userid) ON DELETE DELETE ON UPDATE UPDATE)
        CREATE TABLE IF NOT EXISTS messenger.message (messageid integer PRIMARY KEY DEFAULT nextval('serial'), sender integer, time timestamp without timezone, text text, chatid integer) WHERE table_constraint is: FOREIGN KEY sender REFERENCES user (userid) ON DELETE DELETE ON UPDATE UPDATE chatid REFERENCES chat (chatid) ON DELETE DELETE ON UPDATE UPDATE)
        CREATE TABLE IF NOT EXISTS messenger.chat_participants (chatid integer PRIMARY KEY DEFAULT nextval('serial'), participant integer) WHERE table_constraint is: FOREIGN KEY participant REFERENCES user (userid) ON DELETE DELETE ON UPDATE UPDATE)
        CREATE TABLE IF NOT EXISTS messenger.contacts (userid integer PRIMARY KEY DEFAULT nextval('serial'), contact integer) WHERE table_constraint is: FOREIGN KEY contact REFERENCES user (userid) ON DELETE DELETE ON UPDATE UPDATE)
        """)
cur.execute("""DELETE FROM messenger.contacts;""")
cur.execute("""DELETE FROM messenger.chat_participants;""")
cur.execute("""DELETE FROM messenger.message;""")
cur.execute("""DELETE FROM messenger.chat;""")
cur.execute("""DELETE FROM messenger.user;""")

conn.commit()


Alice = User('Alice', '1111111')
Bob = User('Bob', '2222222')
Ted = User('Ted', '3333333')
Fred = User('Fred', '4444444')
Alice.addContact(Bob)
Alice.addContact(Ted)
Alice.addContact(Fred)
Alice.getContacts()
Bob.addContact(Ted)
Bob.getContacts()
Alice.startChat(Bob, Ted, Fred)


