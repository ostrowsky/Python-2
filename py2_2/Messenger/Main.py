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
Alice.startChat(Bob, Ted)


