from message.message_template.abstrac_message import MessageTemplate


class RabbieTemplate(MessageTemplate):

    #  - - - - - - - - - - - - - - - - -
    # | MESSAGE  -  CLIENT  -  MESSAGE  |
    # |  DATE    -    ID    -   DATA    |
    #  - - - - - - - - - - - - - - - - -
    def set_template(self, message_date, client_id, message_data, relay):
        message = {
            'date': message_date.strftime('%Y/%m/%d'),
            'client_id': client_id,
            'data': message_data,
            'relay': relay,
        }
        return str(message)
