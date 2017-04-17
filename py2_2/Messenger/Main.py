from User import User
from Message import Mess

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

Alice.send_message(Bob, "Привет! Добавь меня в свой список контактов")
Ted.addContact(Bob)
Ted.send_message(Bob, "Привет! Я Ted. Помнишь меня?")
Bob.send_message(Ted, "Привет! Давно не виделись!")
Bob.addContact(Alice)
Bob.getContacts()
Bob.send_message(Alice, "Ты кто?")
Alice.send_message(Bob, "Я Alice")
Bob.send_message(Alice, "Привет, Alice. Добавил тебя")
Ted.send_message(Bob, "Как дела?")
Ted.getChat(Alice)