from message.encryption.encoder.encoder import Encoder
from message.message_template.abstrac_message import MessageTemplate


class Message:
    def __init__(self, template: MessageTemplate, encoder: Encoder):
        self.template = template
        self.encoder = encoder

    def generate_message(self, send_date, message_date, client_id, message_data):
        content = self.template.set_template(send_date=send_date, message_date=message_date, client_id=client_id,
                                             message_data=message_data)

        encoded_message = self.encoder.encode(content)

        return encoded_message
