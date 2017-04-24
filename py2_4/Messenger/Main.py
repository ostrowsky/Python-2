from User import User
from Message import Mess
from Chat import Chat
import psycopg2
from tkinter import *


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

current_chat = 0

current_user = usr1

root = Tk()
root.title("Messenger" + ' --- ' + str(current_user.name))
root.minsize(500,500)
root.resizable(width=True, height=True)
f1 = Frame(root)
f2 = Frame(root)

f1.pack(side='left')
f2.pack(side='right')

contacts_list = Text(f1, bg="white", font="Arial 12", width=20, height=25)
contacts_list.pack(side='bottom')
chat_log = Text(f2, bg="white", font="Arial 12", width=50, height=20)
chat_log.pack(side='top')



def start_chat():
    global current_chat
    contacts_list.delete('0.0', END)
    rows = current_user.getContacts()
    for row in rows:
        contacts_list.insert('1.0',row[0] + "\n")

    current_chat = current_user.startChat(usr2, usr3, usr4, usr5, usr6)


def send_message(event, message_input):
    new_message = message_input.get('0.0', END)
    for chat in Chat.chats:
        if chat.id == current_chat:
            chat.addMessage(current_user, new_message)
        message_input.delete('0.0', END)
    conn_string = "host='localhost' dbname='postgres' user='postgres' password='4309344'"
    conn = psycopg2.connect(conn_string)
    cur = conn.cursor()
    cur.execute(
        """select m.*, u.name from messenger.message m join messenger.user u on m.sender=u.userid where chatid=%s order by time desc;""",
        (current_chat,))
    messages = cur.fetchall()
    conn.commit()
    chat_log.delete('0.0', END)
    for message in messages:
        sender = message[1]
        time = message[2]
        text = message[3] + "\n"
        name = message[-1]
        concat_str = name + ' ' + str(time)[:-7] + "\n"
        chat_log.insert('1.0', text)
        chat_log.insert('1.0',concat_str)

get_contacts = Button(f1, text='Создать чат', command=start_chat)
get_contacts.pack(side='top')
message_input = Text(f2, bg="white", font="Arial 12", width=50, height=5)
message_input.pack(side='bottom')


send_button = Button(f2, text='Отправить сообщение')
send_button.pack(side='bottom')
send_button.bind("<Button-1>", lambda event: send_message(event, message_input))



root.mainloop()




'''
time = mes.time
    chat_log.insert('1.0', current_user.name + str(time)[:-7], '\n')
    chat_log.insert('1.0', new_message, '\n'
'''
