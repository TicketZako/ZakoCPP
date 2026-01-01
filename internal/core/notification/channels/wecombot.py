from apprise import Apprise

from internal.config import configer
from internal.core.notification.channels.base import AppriseNotificationChannel


class WeComBot(AppriseNotificationChannel):
    """
    WeCom Bot 通知
    """

    protocol = "wecombot"

    @classmethod
    def add(cls, queue: Apprise) -> bool:
        """
        添加至队列

        :return bool: 添加成功与否

        :template:
            "{schema}://{key}",
        """
        if cls.protocol not in configer.notification.methods:
            return False

        if not configer.notification.wecombot.bot_key:
            return False

        url = f"{cls.protocol}://{configer.notification.wecombot.bot_key}"

        return queue.add(url)
