from apprise import Apprise

from internal.config import configer
from internal.core.notification.channels.base import AppriseNotificationChannel


class Gotify(AppriseNotificationChannel):
    """
    Gotify 通知
    """

    protocol = "gotify"

    @classmethod
    def add(cls, queue: Apprise) -> bool:
        """
        添加至队列

        :return bool: 添加成功与否

        :template:
            "{schema}://{host}/{token}"
            "{schema}://{host}:{port}/{token}"
            "{schema}://{host}{path}{token}"
            "{schema}://{host}:{port}{path}{token}"
        """
        if cls.protocol not in configer.notification.methods:
            return False

        if not configer.notification.gotify.token:
            return False

        if not configer.notification.gotify.host:
            return False

        use_tls = configer.notification.gotify.use_tls

        # 根据是否使用 SSL/TLS 选择协议
        protocol = "gotifys" if use_tls else "gotify"

        url = f"{protocol}://{configer.notification.gotify.host}"

        # 如果配置了自定义主机，使用自定义主机格式
        if configer.notification.gotify.port:
            url += f":{configer.notification.gotify.port}"

        # 如果配置了自定义路径，使用自定义路径格式
        if configer.notification.gotify.path != "/":
            url += f"{configer.notification.gotify.path}"
        else:
            url += "/"

        # 添加 Token
        url += f"{configer.notification.gotify.token}"

        return queue.add(url)
