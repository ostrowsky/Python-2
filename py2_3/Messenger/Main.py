from User import User
from Message import Mess
from Chat import Chat
import psycopg2

'''
В данной версии реализуется базовый функционал приложения Messenger
(без реализации сетевого взаимодействия)
по созданию объектно-ориентированной модели пользователей и сообщений,
добавлению пользователей к списку контактов,
отправке сообщений и отображения их истории

20.04.17 - Добавлено взаимодействие с СУБД PostgreSQL
'''
conn_string = "host='localhost' dbname='postgres' user='postgres' password='4309344'"
conn = psycopg2.connect(conn_string)
cur = conn.cursor()
cur.execute("""DELETE FROM messenger.contacts;""")
cur.execute("""DELETE FROM messenger.chat_participants;""")
cur.execute("""DELETE FROM messenger.message;""")
cur.execute("""DELETE FROM messenger.chat;""")
cur.execute("""DELETE FROM messenger.user;""")

conn.commit()


Alice = User('Alice', '1111111')
Bob = User('Bob', '2222222')
Ted = User('Ted', '3333333')
Fred = User('Fred', '4444444')
Alice.addContact(Bob)
Alice.addContact(Ted)
Alice.addContact(Fred)
Alice.getContacts()
Bob.addContact(Ted)
Bob.getContacts()
Alice.startChat(Bob, Ted, Fred)


