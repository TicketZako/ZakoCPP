from internal.config import configer
from internal.core.notification import queue


class PushPlus:
    """
    PushPlus 通知
    """

    protocol = "pushplus"

    @staticmethod
    def add() -> bool:
        """
        添加至队列

        :return bool: 添加成功与否
        """
        if PushPlus.protocol not in configer.notification.notifyMethod:
            return False

        if not configer.notification.pushplus.token:
            return False

        url = f"{PushPlus.protocol}://{configer.notification.pushplus.token}"

        return queue.add(url)
