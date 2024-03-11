import abc
from abc import ABC


class MessageEncoder(ABC):

    @abc.abstractmethod
    def encode(self, content):
        ...
