from urllib.parse import quote

from apprise import Apprise

from internal.config import configer
from internal.core.notification.channels.base import AppriseNotificationChannel


class Email(AppriseNotificationChannel):
    """
    Email 通知
    """

    protocol = "mailto"

    @classmethod
    def add(cls, queue: Apprise) -> bool:
        """
        添加至队列

        :return bool: 添加成功与否

        :template:
            "{schema}://{host}"
            "{schema}://{host}:{port}"
            "{schema}://{host}/{targets}"
            "{schema}://{host}:{port}/{targets}"
            "{schema}://{user}@{host}"
            "{schema}://{user}@{host}:{port}"
            "{schema}://{user}@{host}/{targets}"
            "{schema}://{user}@{host}:{port}/{targets}"
            "{schema}://{user}:{password}@{host}"
            "{schema}://{user}:{password}@{host}:{port}"
            "{schema}://{user}:{password}@{host}/{targets}"
            "{schema}://{user}:{password}@{host}:{port}/{targets}"
        """
        if cls.protocol not in configer.notification.methods:
            return False

        if not configer.notification.email.smtp_host:
            return False

        if not configer.notification.email.smtp_user:
            return False

        if not configer.notification.email.smtp_pass:
            return False

        if not configer.notification.email.to_addr:
            return False

        smtp_user = configer.notification.email.smtp_user
        smtp_pass = configer.notification.email.smtp_pass
        smtp_host = configer.notification.email.smtp_host
        smtp_port = configer.notification.email.smtp_port
        use_tls = configer.notification.email.use_tls

        # 根据是否使用 TLS/SSL 选择协议
        protocol = "mailtos" if use_tls else "mailto"

        # 对用户名和密码进行 URL 编码
        url = f"{protocol}://{quote(smtp_user, safe='')}:{quote(smtp_pass, safe='')}@{smtp_host}:{smtp_port}"

        # 添加收件人
        to_emails = configer.notification.email.to_addr
        if isinstance(to_emails, str):
            to_emails = [to_emails]
        to_param = ",".join(to_emails)

        # 添加可选参数
        params = {"to": to_param}
        if configer.notification.email.from_addr:
            params["from"] = configer.notification.email.from_addr

        # 编码参数值
        param_strings = [f"{k}={quote(str(v), safe='')}" for k, v in params.items()]
        url = f"{url}?{'&'.join(param_strings)}"

        return queue.add(url)
