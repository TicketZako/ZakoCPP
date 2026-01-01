from apprise import Apprise

from internal.config import configer
from internal.core.notification.channels.base import AppriseNotificationChannel


class PushMe(AppriseNotificationChannel):
    """
    PushMe 通知
    """

    protocol = "pushme"

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

        if not configer.notification.pushme.token:
            return False

        url = f"{cls.protocol}://{configer.notification.pushme.token}"

        return queue.add(url)
