from message.message_template.abstrac_message import MessageTemplate


class RabbieTemplate(MessageTemplate):

    # --------------------------------------------
    # | SEND  |  MESSAGE  |  CLIENT  |  MESSAGE  |
    # | DATE  |   DATE    |    ID    |   DATA    |
    # --------------------------------------------
    def get_template(self):
        message = f'{self.send_date}{self.message_date}{self.client_id}{self.message_data}'
        return message
