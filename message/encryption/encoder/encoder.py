import abc
from abc import ABC


class Encoder(ABC):

    @abc.abstractmethod
    def encode(self, content):
        ...
