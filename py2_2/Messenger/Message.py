from datetime import datetime


class Mess:
    messages = []

    def __init__(self, sender, recipient, text):
        if Mess.messages:
            self.id = Mess.messages[-1].id + 1
        else:
            self.id = 1
        self.sender = sender
        self.recipient = recipient
        self.text = text
        self.time = datetime.now()
        Mess.messages.append(self)
        self.recipient.receive_message(self)

    def __str__(self):
        return "to: {0} at: {1} from: {2} received text:  {3}".format(self.recipient, self.time, self.sender.name, self.text)
