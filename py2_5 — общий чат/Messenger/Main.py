from User import User
from Message import Mess
from Chat import Chat
from Client import *
import psycopg2
from tkinter import *
import threading

'''
В данной версии реализуется базовый функционал приложения Messenger
(без реализации сетевого взаимодействия)
по созданию объектно-ориентированной модели пользователей и сообщений,
добавлению пользователей к списку контактов,
отправке сообщений и отображения их истории

20.04.17 - Добавлено взаимодействие с СУБД PostgreSQL

24.04.17 - Добавлен функционал создания чата, отправки и отображения истории сообщений в Tkinter
'''
conn_string = "host='localhost' dbname='postgres' user='postgres' password='4309344'"
conn = psycopg2.connect(conn_string)
cur = conn.cursor()
cur.execute("""
        DROP TABLE IF EXISTS messenger.contacts;
        DROP TABLE IF EXISTS messenger.message;
        DROP TABLE IF EXISTS messenger.chat_participants;
        DROP TABLE IF EXISTS messenger.chat;
        DROP TABLE IF EXISTS messenger.user;
        CREATE SCHEMA IF NOT EXISTS messenger;
        CREATE TABLE IF NOT EXISTS messenger.user (userid serial PRIMARY KEY, name varchar(45), password varchar(256), status varchar(45), createdat timestamp);
        CREATE TABLE IF NOT EXISTS messenger.chat (chatid serial PRIMARY KEY, owner integer REFERENCES messenger.user (userid), createdat timestamp);
        CREATE TABLE IF NOT EXISTS messenger.message (messageid serial PRIMARY KEY, sender integer REFERENCES messenger.user (userid), time timestamp, text text, chatid integer REFERENCES messenger.chat (chatid));
        CREATE TABLE IF NOT EXISTS messenger.chat_participants (chatid integer REFERENCES messenger.chat (chatid), participant integer REFERENCES messenger.user (userid));
        CREATE TABLE IF NOT EXISTS messenger.contacts (userid integer REFERENCES messenger.user (userid), contact integer REFERENCES messenger.user (userid));
        """)
conn.commit()
conn.close()

usr1 = User('Alice', '1111111')
usr2 = User('Ted', '2222222')
usr3 = User('Bob', '3333333')
usr4 = User('Fred', '4444444')
usr5 = User('Ed', '555555')
usr6 = User('Bob', '6666666')

usr1.addContact(usr2)
usr1.addContact(usr3)
usr1.addContact(usr4)
usr1.addContact(usr5)
usr1.addContact(usr6)

usr2.addContact(usr1)
usr2.addContact(usr3)
usr2.addContact(usr4)


def start_clients(user, chat):
    new_client = Client(user, chat)

def start_chat(user):
    tuple_contacts = user.getContacts()
    contacts = []
    for x in tuple_contacts:
        contacts.append(x[0])
    print("Контакты ", contacts, "Юзера ", user.name)
    chat_id = user.startChat(contacts)
    print("Чаты ", chat_id, "созданы юзером ", user.name)
    thread_new_chat = threading.Thread(target=start_clients, args=(user, chat_id))
    thread_new_chat.start()


def connect_to_chat(user):
    conn_string = "host='localhost' dbname='postgres' user='postgres' password='4309344'"
    conn = psycopg2.connect(conn_string)
    cur = conn.cursor()
    cur.execute("""select chatid from messenger.chat_participants where participant=%s;""",
    (user.id,))
    chats = cur.fetchall()
    conn.close()
    print("Чаты  ", chats, "с участием юзера ", user.name)
    for chat in chats:
        thread_connect = threading.Thread(target=start_clients, args=(user, chat[0]))
        thread_connect.start()

start_chat(usr1)
connect_to_chat(usr2)





