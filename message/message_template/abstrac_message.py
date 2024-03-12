import abc
from abc import ABC


class MessageTemplate(ABC):



    @abc.abstractmethod
    def set_template(self, message_date, client_id, message_data):
        """
        تابع get_template برای بازگرداندن الگوی پیام استفاده می‌شود.
        """
        ...
        