from User import User
from Message import Mess
from Chat import Chat
import psycopg2
from tkinter import *
from datetime import datetime
import threading


class Client:
    def __init__(self, user):
        self.current_chat = 0
        self.current_user = user
        root = Tk()
        root.title("Messenger" + ' --- ' + self.current_user.name)
        root.minsize(500, 500)
        root.resizable(width=True, height=True)
        f1 = Frame(root)
        f2 = Frame(root)
        f1.pack(side='left')
        f2.pack(side='right')
        self.contacts_list = Text(f1, bg="white", font="Arial 12", width=20, height=25)
        self.contacts_list.pack(side='bottom')
        self.chat_log = Text(f2, bg="white", font="Arial 12", width=50, height=20)
        self.chat_log.pack(side='top')
        get_contacts = Button(f1, text='Создать чат', command=self.start_chat)
        get_contacts.pack(side='top')
        message_input = Text(f2, bg="white", font="Arial 12", width=50, height=5)
        message_input.pack(side='bottom')
        send_button = Button(f2, text='Отправить сообщение')
        send_button.pack(side='bottom')
        send_button.bind("<Button-1>", lambda event: self.send_message(event, message_input))
        print = threading.Thread(target=self.print_chat)
        print.start()
        root.mainloop()


    def print_chat(self):
        while True:
            conn_string = "host='localhost' dbname='postgres' user='postgres' password='4309344'"
            conn = psycopg2.connect(conn_string)
            cur = conn.cursor()
            cur.execute(
                """select m.*, u.name from messenger.message m join messenger.user u on m.sender=u.userid where chatid=%s order by time desc;""",
                (self.current_chat,))
            messages = cur.fetchall()
            conn.commit()
            self.chat_log.delete('0.0', END)
            if messages:
                for message in messages:
                    id = message[0]
                    sender = message[1]
                    time = message[2]
                    text = message[3] + "\n"
                    name = message[-1]
                    name_time = name + ' ' + str(time)[:-7] + "\n"
                    self.chat_log.insert('1.0', text)
                    self.chat_log.insert('1.0', name_time)


    def start_chat(self):
        self.contacts_list.delete('0.0', END)
        rows = self.current_user.getContacts()
        contacts = []
        for row in rows:
            self.contacts_list.insert('1.0',row[0] + "\n")
            contacts.append(row[1])
        self.current_chat = self.current_user.startChat(contacts)


    def send_message(self, event, message_input):
        new_message = message_input.get('0.0', END)
        for chat in Chat.chats:
            if chat.id == self.current_chat:
                chat.addMessage(self.current_user, new_message)
                message_input.delete('0.0', END)





