import textwrap

from dev.dev_print import print_dev

class Message:
    def __init__(self, text, color=(255, 255, 255)):
        self.text = text
        self.color = color

    def to_json(self):
        print('Saving: Game Messages')
        json_data = {
            'text': self.text,
            'color': self.color
        }

        return json_data

    @staticmethod
    def from_json(json_data):
        text = json_data.get('text')
        color = json_data.get('color')

        if color:
            message = Message(text, color)
        else:
            message = Message(text)

        return message
    

class MessageLog:
    def __init__(self, x, width, height, max_messages = 200, number = 0, index = 1):
        self.messages = []
        self.x = x
        self.width = width
        self.height = height
        self.max_messages = max_messages
        self.number = number
        self.index = index

    def add_message(self, message):
        # Split the message if necessary, among multiple lines
        new_msg_lines = textwrap.wrap(message.text, self.width)
        
        for line in new_msg_lines:
            #print_dev('Printing message: {0}'.format(message.text))
            # If the buffer is full, remove the first line to make room for the new one
            if len(self.messages) == self.max_messages:
                del self.messages[0]
                self.number -= 1
                self.index -= 1

            # Add the new line as a Message object, with the text and the color
            self.messages.append(Message(line, message.color))
            self.number += 1
            self.index_message(1)

            #print_dev('Total messages: {0}'.format(self.number))

    def index_message(self, num):
        index = self.index + num

        # uses magic numbers (menu height=6) to determine bounds of index scrolling
        if self.number <= 6 or index < 1:
            index = 1
        elif index + 5 > self.number:
            index -= num

        if index > self.max_messages:
            index = self.max_messages - 6
        #print('Indexing message by {0}; New index {1}'.format(num, self.index))

        self.index = index
        return

    def to_json(self):
        json_data = {
            'x': self.x,
            'width': self.width,
            'height': self.height,
            'messages': [message.to_json() for message in self.messages],
            'max_messages': self.max_messages,
            'number': self.number,
            'index': self.index
        }

        return json_data

    @staticmethod
    def from_json(json_data):
        x = json_data.get('x')
        width = json_data.get('width')
        height = json_data.get('height')
        messages_json = json_data.get('messages')
        max_messages = json_data.get('max_messages')
        number = json_data.get('number')
    
        message_log = MessageLog(x, width, height)

        for message_json in messages_json:
            message_log.add_message(Message.from_json(message_json))

        return message_log
    
