from apprise import Apprise

from internal.config import configer
from internal.core.notification.channels.base import AppriseNotificationChannel


class PushDeer(AppriseNotificationChannel):
    """
    PushDeer 通知
    """

    protocol = "pushdeer"

    @classmethod
    def add(cls, queue: Apprise) -> bool:
        """
        添加至队列

        :return bool: 添加成功与否

        :template:
            "{schema}://{pushkey}"
            "{schema}://{host}/{pushkey}"
            "{schema}://{host}:{port}/{pushkey}"
        """
        if cls.protocol not in configer.notification.methods:
            return False

        if not configer.notification.pushdeer.push_key:
            return False

        push_key = configer.notification.pushdeer.push_key
        use_ssl = configer.notification.pushdeer.use_tls

        # 根据是否使用 SSL/TLS 选择协议
        protocol = "pushdeers" if use_ssl else "pushdeer"

        # 如果配置了自定义主机，使用自定义主机格式
        if configer.notification.pushdeer.host:
            host = configer.notification.pushdeer.host
            port = configer.notification.pushdeer.port

            if port:
                url = f"{protocol}://{host}:{port}/{push_key}"
            else:
                url = f"{protocol}://{host}/{push_key}"

        # 使用默认服务
        else:
            url = f"{protocol}://{push_key}"

        return queue.add(url)
