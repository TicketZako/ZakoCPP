from internal.config import configer
from internal.core.notification import queue


class Bark:
    """
    Bark 通知
    """

    protocol = "bark"

    @staticmethod
    def add() -> bool:
        """
        添加至队列

        :return bool: 添加成功与否
        """
        if Bark.protocol not in configer.notification.notifyMethod:
            return False

        if not configer.notification.bark.token:
            return False

        url = f"{Bark.protocol}://{configer.notification.bark.token}"
        params = {
            "level": configer.notification.bark.level,
        }
        url = f"{url}?{'&'.join([f'{k}={v}' for k, v in params.items()])}"

        return queue.add(url)
