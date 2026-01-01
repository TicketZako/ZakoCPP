from pydantic import BaseModel, Field

from internal.config import configer
from internal.util import PrivacyUtils


class NotificationContent(BaseModel):
    """
    通知内容
    """

    title: str = Field(
        default_factory=lambda: NotificationContentProvider.title(), description="标题"
    )
    body: str = Field(
        default_factory=lambda: NotificationContentProvider.body(), description="内容"
    )


class NotificationContentProvider(BaseModel):
    """
    通知内容提供器
    """

    @staticmethod
    def title() -> str:
        """
        获取标题

        :return str: 标题
        """
        title = "Cpp Ticketer"
        return title

    @staticmethod
    def body() -> str:
        """
        获取内容

        :return str: 内容
        """
        body = [
            "账号：{}".format(PrivacyUtils.mask_phone(configer.account.account)),
            "购票人：{}".format(",".join([b.realname for b in configer.buyer.buyer])),
            "票档：{}".format(
                " ".join(
                    [
                        configer.product.ticketMain.name,
                        configer.product.ticketType.square,
                        configer.product.ticketType.name,
                    ]
                )
            ),
        ]
        return "\n".join(body)
