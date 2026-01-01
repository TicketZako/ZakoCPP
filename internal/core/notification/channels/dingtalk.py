from apprise import Apprise

from internal.config import configer
from internal.core.notification.channels.base import AppriseNotificationChannel


class DingTalk(AppriseNotificationChannel):
    """
    钉钉通知
    """

    protocol = "dingtalk"

    @classmethod
    def add(cls, queue: Apprise) -> bool:
        """
        添加至队列

        :return bool: 添加成功与否

        :template:
            "{schema}://{token}/"
            "{schema}://{token}/{targets}/"
            "{schema}://{secret}@{token}/"
            "{schema}://{secret}@{token}/{targets}/"
        """
        if cls.protocol not in configer.notification.methods:
            return False

        if not configer.notification.dingtalk.token:
            return False

        url = f"{cls.protocol}://{configer.notification.dingtalk.token}"

        return queue.add(url)
