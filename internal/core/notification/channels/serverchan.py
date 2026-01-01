from apprise import Apprise

from internal.config import configer
from internal.core.notification.channels.base import AppriseNotificationChannel


class ServerChan(AppriseNotificationChannel):
    """
    ServerChan 通知
    """

    protocol = "schan"

    @classmethod
    def add(cls, queue: Apprise) -> bool:
        """
        添加至队列

        :return bool: 添加成功与否

        :template:
            "{schema}://{token}"
        """
        if cls.protocol not in configer.notification.methods:
            return False

        if not configer.notification.serverchan.token:
            return False

        url = f"{cls.protocol}://{configer.notification.serverchan.token}"

        return queue.add(url)
