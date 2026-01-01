from apprise import Apprise

from internal.config import configer
from internal.core.notification.channels.base import AppriseNotificationChannel


class Slack(AppriseNotificationChannel):
    """
    Slack 通知
    """

    protocol = "slack"

    @classmethod
    def add(cls, queue: Apprise) -> bool:
        """
        添加至队列

        :return bool: 添加成功与否

        :template:
            # Webhook
            "{schema}://{token_a}/{token_b}/{token_c}",
            "{schema}://{botname}@{token_a}/{token_b}{token_c}",
            "{schema}://{token_a}/{token_b}/{token_c}/{targets}",
            "{schema}://{botname}@{token_a}/{token_b}/{token_c}/{targets}",
            # OAuth Bot
            "{schema}://{access_token}/",
            "{schema}://{access_token}/{targets}",
        """
        if cls.protocol not in configer.notification.methods:
            return False

        # Webhook 方式 (token_a, token_b, token_c)
        if configer.notification.slack.token_a:
            if (
                not configer.notification.slack.token_b
                or not configer.notification.slack.token_c
            ):
                return False

            token_a = configer.notification.slack.token_a
            token_b = configer.notification.slack.token_b
            token_c = configer.notification.slack.token_c

            url = f"{cls.protocol}://{token_a}/{token_b}/{token_c}"

        # OAuth 方式 (oauth_token)
        elif configer.notification.slack.oauth_token:
            oauth_token = configer.notification.slack.oauth_token
            url = f"{cls.protocol}://{oauth_token}/"

        else:
            return False

        return queue.add(url)
