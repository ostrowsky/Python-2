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
        self.root = Tk()
        self.current_user = user
        self.root.title('Messenger' + ' --- ' + self.current_user.name + ' ('+str(self.current_user.id) + ')')
        self.root.minsize(500, 500)
        self.root.resizable(width=True, height=True)
        self.left_part = Frame(self.root)
        self.right_part = Frame(self.root)
        self.left_part.pack(side='left')
        self.right_part.pack(side='right')
        add_cont_button = Button(self.left_part, text='Добавить контакт', command=self.contact_input)
        add_cont_button.pack(side='top')
        self.contacts_list = Frame(self.left_part)
        self.contacts_list.pack(side='top')
        chat_log = Text(self.right_part, bg="white", font="Arial 12", width=50, height=20)
        chat_log.pack(side='top')
        message_input = Text(self.right_part, bg="white", font="Arial 12", width=50, height=5)
        message_input.pack(side='bottom')
        send_button = Button(self.right_part, text='Отправить сообщение')
        send_button.pack(side='bottom')
        self.update_contacts()
        self.root.mainloop()

    def update_contacts(self):
        self.contacts_list.destroy()
        self.contacts_list = Frame(self.left_part)
        self.contacts_list.pack(side='top')
        contacts = self.current_user.getContacts()
        if contacts:
            for contact in contacts:
                cont_field = Frame(self.contacts_list)
                cont_field.pack(side='top')
                cont_name = Text(cont_field, bg="white", font="Arial 10", width=20, height=2)
                cont_name.pack(side='left')
                cont_name.insert('0.0', contact[2])
                start_chat = Button(cont_field, text='Начать чат', command=lambda contact: start_chat(contact[0]))
                start_chat.pack(side='right')

    def start_chat(self, contact_id):
        self.current_user.startChat(id)

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
                self.update_contacts()


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

