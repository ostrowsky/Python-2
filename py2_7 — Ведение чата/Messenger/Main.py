from User import User
from Message import Mess
from Chat import Chat
from Client import *
import pymysql.cursors
#import psycopg2
from tkinter import *
import threading
import hashlib
from db_config import *
'''
В данной версии реализуется базовый функционал приложения Messenger
(без реализации сетевого взаимодействия)
по созданию объектно-ориентированной модели пользователей и сообщений,
добавлению пользователей к списку контактов,
отправке сообщений и отображения их истории

20.04.17 - Добавлено взаимодействие с СУБД PostgreSQL

24.04.17 - Добавлен функционал создания чата, отправки и отображения истории сообщений в Tkinter

27.04.17 - Проект переведен на СУБД MySQL, реализовано многопоточное отображение истории сообщений общего чата в нескольких клиентских теримналах, а также отправка сообщений.


28.04.17 - Добавлена аутентификация и авторизация

11.05.17 - Реализовано добавление в список контактов

16.05.17 - Реализовано ведение двустороннего чата
'''
conn = pymysql.connect(host=HOST,
                               user=USER,
                               password=PASSWORD,
                               db=DB,
                               charset=CHARSET,
                               cursorclass=CURSORCLASS)
cur = conn.cursor()

cur.execute("""
        DROP TABLE IF EXISTS messenger.contacts;
        DROP TABLE IF EXISTS messenger.message;
        DROP TABLE IF EXISTS messenger.chat_participants;
        DROP TABLE IF EXISTS messenger.chat;
        DROP TABLE IF EXISTS messenger.user;
        CREATE SCHEMA IF NOT EXISTS messenger;
        CREATE TABLE IF NOT EXISTS messenger.user (userid serial PRIMARY KEY, name varchar(45) COLLATE utf8_bin, password varchar(256), status varchar(45), createdat timestamp);
        CREATE TABLE IF NOT EXISTS messenger.chat (chatid serial PRIMARY KEY, owner integer REFERENCES messenger.user (userid), createdat timestamp);
        CREATE TABLE IF NOT EXISTS messenger.message (messageid serial PRIMARY KEY, sender integer REFERENCES messenger.user (userid), time timestamp, text text COLLATE utf8_bin, chatid integer REFERENCES messenger.chat (chatid));
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
    if login not in [user['name'] for user in User.getUsersList()]:
        output.delete('0.0', END)
        output.insert('1.0', 'Ошибка! Пользователь с именем {} не зарегистрирован \n'.format(login))
    else:
        for user in User.getUsersList():
            if (login, passw) == (user['name'], user['password']):
                print(user['userid'])
                authorized_user = User.getUserById(user['userid'])
                new_client = Client(authorized_user)
            elif login == user['name'] and passw != user['password']:
                output.delete('0.0', END)
                output.insert('1.0', 'Ошибка! Неверный пароль для пользователя с именем {} \n'.format(login))



def registrate():
    output.delete('0.0', END)
    login = log_field.get()
    passw = pass_field.get()
    if login not in [user['name'] for user in User.getUsersList()]:
        new_user = User(login, passw)
        new_user.save()
        output.delete('0.0', END)
        output.insert('1.0', 'Пользователь успешно зарегистрирован\n')
    else:
        output.delete('0.0', END)
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



