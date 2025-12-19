from internal.config import configer
from internal.core.notification import queue
from internal.core.notification.channels import Bark, PushPlus
from internal.core.notification.content import NotificationContent
from internal.util import log


class NotificationPusher:
    """
    推送通知
    """

    channels = [
        PushPlus,
        Bark,
    ]

    @staticmethod
    def _add() -> None:
        """
        添加至队列
        """
        for method in configer.notification.notifyMethod:
            for channel in NotificationPusher.channels:
                if method == channel.protocol:
                    result = channel.add()
                    if result:
                        log.info(f"添加 {method} 渠道至队列成功")
                    else:
                        log.error(f"添加 {method} 渠道至队列失败")

    @staticmethod
    def _send() -> bool:
        """
        发送通知

        :return bool: 发送成功与否
        """
        content = NotificationContent(
            title="Cpp Ticketer",
            body="\n".join(
                [
                    "账号：{}".format(configer.account.account),
                    "购票人：{}".format(
                        ",".join([b.realname for b in configer.buyer.buyer])
                    ),
                    "票档：{}".format(
                        " ".join(
                            [
                                configer.product.ticketMain.name,
                                configer.product.ticketType.square,
                                configer.product.ticketType.name,
                            ]
                        )
                    ),
                    "数量：{}".format(configer.buyer.count),
                ]
            ),
        )

        try:
            result = queue.notify(
                title=content.title,
                body=content.body,
            )
            return result

        except Exception as e:
            log.error(f"发送通知失败: {e}")
            return False

    @staticmethod
    def push() -> None:
        """
        推送通知
        """
        if not configer.notification.isEnable:
            return

        if not configer.notification.notifyMethod:
            log.warning("未启用任何通知方式")
            return

        NotificationPusher._add()
        result = NotificationPusher._send()
        if not result:
            log.error("推送通知失败")
