import hashlib
from Message import Mess
from Chat import Chat


class User:
    users_list = []
    status_list = ('offline', 'online')
    user_statuses = {}
    def __init__(self, name, password):
        if User.users_list:
            self.id = User.users_list[-1].id + 1
        else:
            self.id = 111111
        User.users_list.append(self)
        self.name = name
        self.password = hashlib.md5(password.encode('utf-8'))
        self.status = User.status_list[0]
        User.user_statuses[self.id] = User.status_list[0]
        self.contacts = []


    def getId(self):
        return self.id


    def getName(self):
        return self.name


    def getStatus(self):
        return self.status


    def addContact(self, contact):
        if contact in User.users_list:
            self.contacts.append(contact)
            print("Пользователь {} добавлен в список контактов пользователя {}".format(contact.name, self.name))
        else:
            print("Пользователь не зарегистрирован")


    def getContacts(self):
        if self.contacts:
            print("Список контактов пользователя {}: ".format(self.name))
            i = 1
            for contact in self.contacts:
                print("     №{} {}".format(i, contact))
                i+=1
        else:
            print("Список контактов пользователя {} пуст".format(self.name))


    def delFromContacts(self, contact):
       pass


    def connect(self):
        User.user_statuses[self.id] = User.status_list[1]

    def startChat(self):
        pass

    def getChat(self):
        pass


    def receive_message(self, message):
        print("to: {0} at: {1} from: {2} received text:  {3}".format(self.name, message.time, message.sender.name, message.text))


    def __str__(self):
        return "Пользователь с ID: {0}, имя: {1}".format(self.id, self.name)
'''
    def getChat(self, contact):
        print("--------------------Чат с {}-----------------------------".format(contact.name))
        chat_with = []
        for message in Mess.messages:
            if message.recipient == self and message.sender not in chat_with:
                chat_with.append(message.sender)
            if message.sender == self and message.recipient not in chat_with:
                chat_with.append(message.recipient)


        for user in chat_with:
            if user == contact:
                for message in Mess.messages:
                    if message.recipient == user or message.sender == user:
                        if message.sender == self:
                            print(self.name, str(message.time)[:-7])
                            print("{0:<}".format(message.text))
                        if message.recipient == self:
                            concat_str = str(message.time)[:-7] + ' ' + message.sender.name
                            print("{0:>50}".format(concat_str))
                            print("{0:>50}".format(message.text))
            else:
                print("Чат с такими участниками не найден")
                print('\n')









        mess_dict = {}
        for message in Mess.messages:
            if not message.sender == self:
                mess_dict[message.sender] =  message

        print(mess_dict)
        for key, value in mess_dict.items():
            print("--------------------Чат с {}-----------------------------".format(key.name))
            if value.sender == self:
                print(self.name, str(message.time)[:-7])
                print("{0:<}".format(message.text))
            if value.recipient == self:
                concat_str = str(message.time)[:-7] + ' ' + message.sender.name
                print("{0:>50}".format(concat_str))
                print("{0:>50}".format(message.text))
'''