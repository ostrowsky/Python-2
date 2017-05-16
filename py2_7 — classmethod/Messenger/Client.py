from User import User
from Message import Mess
from Chat import Chat
#import psycopg2
import pymysql.cursors
from tkinter import *
from datetime import datetime
import threading


class Client:

    def __init__(self, user):
        root = Tk()
        self.current_user = user
        root.title('Messenger' + ' --- ' + self.current_user.name + ' ('+str(self.current_user.id) + ')')
        root.minsize(500, 500)
        root.resizable(width=True, height=True)
        f1 = Frame(root)
        f2 = Frame(root)
        f1.pack(side='left')
        f2.pack(side='right')
        contacts_list = Text(f1, bg="white", font="Arial 12", width=20, height=25)
        contacts_list.pack(side='bottom')
        chat_log = Text(f2, bg="white", font="Arial 12", width=50, height=20)
        chat_log.pack(side='top')
        message_input = Text(f2, bg="white", font="Arial 12", width=50, height=5)
        message_input.pack(side='bottom')
        add_cont_button = Button(f1, text='Добавить контакт', command=self.contact_input)
        add_cont_button.pack(side='top')
        send_button = Button(f2, text='Отправить сообщение')
        send_button.pack(side='bottom')
        contacts = self.current_user.getContacts()
        print(contacts)
        for contact in contacts:
            contacts_list.insert('1.0',contact[2])
            contacts_list.insert('1.0','\n')
        root.mainloop()



    def contact_input(self):
        def add_contact():
            cont_id = cont_field.get()
            if cont_id == str(self.current_user.id):
                output.delete('0.0', END)
                output.insert('1.0', 'Нельзя добавить себя в список контактов\n')
            else:
                cont_added = self.current_user.addContact(cont_id)
                output.delete('0.0', END)
                output.insert('1.0', cont_added)



        root = Tk()
        root.title('Добавить контакт ')
        root.minsize(100, 100)
        root.resizable(width=False, height=False)
        f1 = Frame(root)
        f2 = Frame(root)
        f1.pack(side='top')
        f2.pack(side='bottom')
        cont_label = Label(f1, text='Введите ID пользователя')
        cont_field = Entry(f1, )
        add_butt = Button(f1, text='Добавить', command=add_contact)
        output = Text(f2, bg="white", font="Arial 12", width=25, height=5)
        cont_label.pack(side='top')
        cont_field.pack(side='top')
        add_butt.pack(side='top')
        output.pack(side='top')
        root.mainloop()

