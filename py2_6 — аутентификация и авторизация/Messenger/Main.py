from User import User
from Message import Mess
from Chat import Chat
from Client import *
import pymysql.cursors
#import psycopg2
from tkinter import *
import threading
import hashlib

'''
В данной версии реализуется базовый функционал приложения Messenger
(без реализации сетевого взаимодействия)
по созданию объектно-ориентированной модели пользователей и сообщений,
добавлению пользователей к списку контактов,
отправке сообщений и отображения их истории

20.04.17 - Добавлено взаимодействие с СУБД PostgreSQL

24.04.17 - Добавлен функционал создания чата, отправки и отображения истории сообщений в Tkinter

27.04.17 - Проект переведен на СУБД MySQL, реализовано многопоточное отображение истории сообщений общего чата в нескольких клиентских теримналах, а также отправка сообщений.
!!! Сообщения на кириллице пока что не поддерживаются !!!

28.04.17 - Добавлена аутентификация и авторизация
'''

conn = pymysql.connect(host='localhost',
                             user='root',
                             password='4309344',
                             db='test',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
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
print("connection sucsess")
conn.commit()
conn.close()

def authenticate():
    output.delete('0.0', END)
    login = log_field.get()
    passw = hashlib.md5(pass_field.get().encode()).hexdigest()
    for user in User.users_list:
        if (login, passw) == (user.name, user.password):
            new_client = Client(user)
    else:
        output.insert('1.0', 'Ошибка! Пользователь с именем {} уже был зарегистрирован\n'.format(login))


def registrate():
    output.delete('0.0', END)
    login = log_field.get()
    passw = pass_field.get()
    if login not in [x.name for x in User.users_list]:
        new_user = User(login, passw)
        output.insert('1.0', 'Пользователь успешно зарегистрирован\n')
    else:
        output.insert('1.0', 'Ошибка! Пользователь с именем {} уже был зарегистрирован\n'.format(login))


root = Tk()
root.title('Messenger' + ' Аутентификация ' )
root.minsize(100, 100)
root.resizable(width=False, height=False)
f1 = Frame(root)
f2 = Frame(root)
f1.pack(side='top')
f2.pack(side='bottom')
log_label = Label(f1,text='Логин')
log_field = Entry(f1,)
pass_label = Label(f1, text='Пароль')
pass_field = Entry(f1, )
auth = Button(f1, text='Войти', command=authenticate)
reg = Button(f1, text='Зарегистрироваться', command=registrate)
output = Text(f2, bg="white", font="Arial 12", width=25, height=5)
log_label.pack(side='top')
log_field.pack(side='top')
pass_label.pack(side='top')
pass_field.pack(side='top')
auth.pack(side='left')
reg.pack(side='right')
output.pack(side='top')
root.mainloop()



'''
usr1 = User('Alice', '1111111')
usr2 = User('Ted', '2222222')
usr3 = User('Bob', '3333333')
usr4 = User('Fred', '4444444')
usr5 = User('Ed', '555555')
usr6 = User('Sad', '6666666')

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
    conn = pymysql.connect(host='localhost',
                           user='root',
                           password='4309344',
                           db='test',
                           charset='utf8mb4',
                           cursorclass=pymysql.cursors.DictCursor)
    cur = conn.cursor()
    cur.execute("""select chatid from messenger.chat_participants where participant=%s;""",
    (user.id,))
    chats = cur.fetchall()
    print(chats)
    conn.close()
    print("Чаты  ", chats, "с участием юзера ", user.name)
    for chat in chats:
        thread_connect = threading.Thread(target=start_clients, args=(user, chat['chatid']))
        thread_connect.start()

start_chat(usr1)
connect_to_chat(usr2)

'''



