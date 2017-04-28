from User import User
from Message import Mess
from Chat import Chat
#import psycopg2
import pymysql.cursors
from tkinter import *
from datetime import datetime
import threading


class Client(threading.Thread):
    def __init__(self, user, chat):
        super().__init__()
        self.current_chat = chat
        self.current_user = user


    def run(self):
        root = Tk()
        root.title('Messenger' + ' --- ' + self.current_user.name + ' ' + 'Чат № ' + str(self.current_chat))
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
        get_contacts = Button(f1, text='Список контактов', command=self.get_contacts)
        get_contacts.pack(side='top')
        message_input = Text(f2, bg="white", font="Arial 12", width=50, height=5)
        message_input.pack(side='bottom')
        send_button = Button(f2, text='Отправить сообщение')
        send_button.pack(side='bottom')
        send_button.bind("<Button-1>", lambda event: self.send_message(event, message_input))
        self.get_contacts()
        new_thread = threading.Thread(target=self.draw_chat)
        new_thread.start()
        root.mainloop()



    def draw_chat(self):
        while True:
            self.chat_log.delete('0.0', END)
            chat_id = self.current_chat
            for chat in Chat.chats:
                if chat.id == chat_id:
                    if chat.getChatMessages():
                        text = chat.getChatMessages()[0]
                        name_time = chat.getChatMessages()[1]
                        self.chat_log.insert('1.0', text)
                        self.chat_log.insert('1.0', name_time)


    def get_contacts(self):
        self.contacts_list.delete('0.0', END)
        rows = self.current_user.getContacts()
        print(rows)

        for row in rows:
            self.contacts_list.insert('1.0',str(row[1]) + "\n")
            #contacts.append(row[0])
        #self.current_chat = self.current_user.startChat(contacts)



    def send_message(self, event, message_input):
        new_message = message_input.get('0.0', END)
        for chat in Chat.chats:
            #if chat.id == self.current_chat:
            chat.addMessage(self.current_user, new_message)
            message_input.delete('0.0', END)





