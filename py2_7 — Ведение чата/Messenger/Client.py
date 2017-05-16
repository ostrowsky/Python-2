from User import User
from Message import Mess
from Chat import Chat
#import psycopg2
import pymysql.cursors
from tkinter import *
from datetime import datetime
import threading
from db_config import *
import time


class Client:

    def __init__(self, user):
        self.root = Tk()
        self.current_user = user
        self.current_chat = None
        self.root.title('Messenger' + ' --- ' + self.current_user.name + ' ('+str(self.current_user.id) + ')')
        self.root.minsize(500, 500)
        self.root.resizable(width=True, height=True)
        self.left_part = Frame(self.root)
        self.right_part = Frame(self.root)
        self.left_part.pack(side='left')
        self.right_part.pack(side='right')
        self.side_block = Frame(self.left_part)
        self.side_block.pack(side='bottom')
        add_cont_button = Button(self.side_block, text='Добавить контакт', command=self.contact_input)
        add_cont_button.pack(side='top')
        self.contacts_list = Frame(self.side_block)
        self.contacts_list.pack(side='top')
        self.chat_log = Text(self.right_part, bg="white", font="Arial 12", width=50, height=20)
        self.chat_log.pack(side='top')
        self.message_input = Text(self.right_part, bg="white", font="Arial 12", width=50, height=5)
        self.message_input.pack(side='bottom')
        self.send_button = Button(self.right_part, text='Отправить сообщение', command=self.send_message)
        self.send_button.pack(side='bottom')
        self.update_contacts()
        new_thread = threading.Thread(target=self.print_chat)
        new_thread.start()
        self.root.mainloop()

    def update_contacts(self):
        self.contacts_list.destroy()
        self.contacts_list = Frame(self.side_block)
        self.contacts_list.pack(side='top')
        contacts = self.current_user.getContacts()
        if contacts:
            for contact in contacts:
                cont_field = Frame(self.contacts_list)
                cont_field.pack(side='top')
                num_mess = Text(cont_field, bg="white", font="Arial 10", width=1, height=1)
                num_mess.pack(side='left')
                cont_name = Text(cont_field, bg="white", font="Arial 10", width=10, height=1)
                cont_name.pack(side='left')
                cont_name.insert('0.0', contact[2])
                start_chat = Button(cont_field, text='Открыть чат', command=lambda x=contact[1]: self.start_chat(x))
                start_chat.pack(side='right')


    def start_chat(self, contact_id):
        participant = User.getUserById(contact_id)
        if Chat.getChatByParticipants(self.current_user, participant):
            self.current_chat = Chat.getChatByParticipants(self.current_user, participant)
        else:
            chat_id = self.current_user.startChat(participant)
            self.current_chat = Chat.getChatById(chat_id)


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


    def send_message(self):
        text = self.message_input.get("1.0", END)
        new_mess = self.current_chat.addMessage(self.current_user, text)
        print(new_mess)
        self.message_input.delete('0.0', END)

    def print_chat(self):

        while True:

            if self.current_chat:
                conn = pymysql.connect(host=HOST,
                                   user=USER,
                                   password=PASSWORD,
                                   db=DB,
                                   charset=CHARSET,
                                   cursorclass=CURSORCLASS)
                cur = conn.cursor()
                cur.execute(
                """select m.*, u.name from messenger.message m join messenger.user u on m.sender=u.userid where chatid=%s order by time desc;""",
                (self.current_chat.id,))
                messages = cur.fetchall()
                conn.commit()
                conn.close()
                self.chat_log.delete('0.0', END)
                if messages:
                    for message in messages:
                        id = message['messageid']
                        sender = message['name']
                        time = message['time']
                        text = message['text'] + "\n"
                        name = message['name']
                        name_time = name+ ' ' + str(time) + "\n"
                        text_str = "{0:<}".format(text)
                        self.chat_log.insert('1.0', text_str)
                        self.chat_log.insert('1.0', name_time)

            else:
                self.chat_log.insert('1.0', 'Сообщений не найдено')
                self.chat_log.delete('0.0', END)