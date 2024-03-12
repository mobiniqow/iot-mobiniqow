import abc
from abc import ABC


class Decoder(ABC):

    @abc.abstractmethod
    def decode(self,payload):
        ...
