import abc
from abc import ABC


class MessageTemplate(ABC):

    def __init__(self, send_date, message_date, client_id, message_data):
        """
        تابع set_message برای تنظیم تاریخ ارسال، تاریخ پیام، شناسه مشتری و داده پیام استفاده می‌شود.
        """
        self.send_date = send_date
        self.message_date = message_date
        self.client_id = client_id
        self.message_data = message_data


    @abc.abstractmethod
    def get_template(self):
        """
        تابع get_template برای بازگرداندن الگوی پیام استفاده می‌شود.
        """
        ...
        