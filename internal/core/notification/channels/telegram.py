from apprise import Apprise

from internal.config import configer
from internal.core.notification.channels.base import AppriseNotificationChannel


class Telegram(AppriseNotificationChannel):
    """
    Telegram 通知
    """

    protocol = "tgram"

    @classmethod
    def add(cls, queue: Apprise) -> bool:
        """
        添加至队列

        :return bool: 添加成功与否

        :template:
            "{schema}://{bot_token}",
            "{schema}://{bot_token}/{targets}",
        """
        if cls.protocol not in configer.notification.methods:
            return False

        if not configer.notification.telegram.bot_token:
            return False

        if not configer.notification.telegram.chat_id:
            return False

        bot_token = configer.notification.telegram.bot_token
        chat_id = configer.notification.telegram.chat_id

        url = f"{cls.protocol}://{bot_token}/{chat_id}"

        return queue.add(url)
