from platform import system
from typing import ClassVar

from apprise import Apprise

from internal.config import configer
from internal.core.notification.channels.base import AppriseNotificationChannel


class Desktop(AppriseNotificationChannel):
    """
    PushPlus 通知
    """

    protocol = "desktop"

    platform_map: ClassVar[dict[str, str]] = {
        "Windows": "windows",
        "Linux": "dbus",
        "Darwin": "macosx",
    }

    @classmethod
    def add(cls, queue: Apprise) -> bool:
        """
        添加至队列

        :return bool: 添加成功与否

        :template:
            "{schema}://"
        """
        if cls.protocol not in configer.notification.methods:
            return False

        url = f"{cls.platform_map[system()]}://"

        return queue.add(url)
