import abc
from abc import ABC

from message.message_template.abstrac_message import MessageTemplate


class MessageEncoder(ABC):
    def __init__(self, message_template: MessageTemplate, secret):
        self.message_template = message_template
        self.secret = secret

    @abc.abstractmethod
    def encode(self):
        ...
