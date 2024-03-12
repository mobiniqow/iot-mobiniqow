from message.encryption.encoder.encoder import Encoder
from message.message_template.abstrac_message import MessageTemplate


class MessageGenerator:
    def __init__(self, template: MessageTemplate, encoder: Encoder):
        self.template = template
        self.encoder = encoder

    def generate(self, message_date, client_id, message_data):
        content = self.template.set_template(message_date=message_date, client_id=client_id,
                                             message_data=message_data)
        encoded_message = self.encoder.encode(content)
        return encoded_message
