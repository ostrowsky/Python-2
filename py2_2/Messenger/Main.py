from User import User
from Message import Mess
from Chat import Chat
'''
В данной версии реализуется базовый функционал приложения Messenger
(без реализации сетевого взаимодействия)
по созданию объектно-ориентированной модели пользователей и сообщений,
добавлению пользователей к списку контактов,
отправке сообщений и отображения их истории
'''

Alice = User('Alice', '1111111')
Bob = User('Bob', '2222222')
Ted = User('Ted', '3333333')
print(Alice)
print(Bob)

Alice.addContact(Bob)
Alice.addContact(Ted)
Alice.getContacts()
Bob.addContact(Ted)
Bob.getContacts()

chat1 = Chat(Alice)
chat1.add_participants(Bob)
chat1.addMessage(Alice, "Привет! Добавь меня в свой список контактов")
Ted.addContact(Bob)
chat2 = Chat(Ted)
chat2.add_participants(Bob)
chat2.addMessage(Ted,"Привет! Я Ted. Помнишь меня?")
chat2.addMessage(Bob, "Привет! Давно не виделись!")
Bob.addContact(Alice)
Bob.getContacts()
chat1.addMessage(Bob,"Ты кто?")
chat1.addMessage(Alice,"Я Alice")
chat1.addMessage(Bob,"Привет, Alice. Добавил тебя")
chat2.addMessage(Ted,"Как дела?")
chat1.printChat()
chat2.printChat()
#Bob.getChat(Ted)
#for chat in Chat.chats: print(chat.owner.name, [participant.name for participant in chat.participants], [message.text for message in chat.messages])


