from apprise import Apprise

from internal.config import configer
from internal.core.notification.channels.base import AppriseNotificationChannel


class Bark(AppriseNotificationChannel):
    """
    Bark 通知
    """

    protocol = "bark"

    @classmethod
    def add(cls, queue: Apprise) -> bool:
        """
        添加至队列

        :return bool: 添加成功与否

        :template:
            "{schema}://{host}/{targets}"
            "{schema}://{host}:{port}/{targets}"
            "{schema}://{user}:{password}@{host}/{targets}"
            "{schema}://{user}:{password}@{host}:{port}/{targets}"
        """
        if cls.protocol not in configer.notification.methods:
            return False

        if not configer.notification.bark.token:
            return False

        url = f"{cls.protocol}://{configer.notification.bark.token}"
        params = {
            "level": configer.notification.bark.level,
        }
        url = f"{url}?{'&'.join([f'{k}={v}' for k, v in params.items()])}"

        return queue.add(url)
