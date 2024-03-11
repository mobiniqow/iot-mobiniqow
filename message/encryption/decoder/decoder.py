import abc
from abc import ABC


class MessageDecoder(ABC):

    @abc.abstractmethod
    def decode(self,payload):
        ...
