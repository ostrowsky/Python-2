class Chat:
    chats = []
    def __init__(self, owner, participant):
        self.owner = owner
        self.participant = participant
        self.messages = []
        Chat.chats.append(self)



    def addMessage(self, message):
        self.messages.append(message)


    def getChat(self, owner):
        for chat in Chat.chats:
            if chat.owner == owner:
                print("--------------------Чат с {}-----------------------------".format(chat.participant))
                for message in chat.messages:
                    if message.sender == self:
                        print(self.name, str(message.time)[:-7])
                        print("{0:<}".format(message.text))
                    if message.recipient == self:
                        concat_str = str(message.time)[:-7] + ' ' + message.sender.name
                        print("{0:>50}".format(concat_str))
                        print("{0:>50}".format(message.text))


    def __str__(self):
        return "Чат пользователя {} с пользователем {}".format(self.owner.name, self.participant.name)