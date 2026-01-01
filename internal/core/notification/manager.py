from collections import deque

from apprise import Apprise

from internal.config import configer
from internal.core.notification import NotificationContent, channels
from internal.core.notification.channels.base import ExternalNotificationChannel
from internal.error import NotificationError
from internal.util import log


class NotificationManager:
    """
    推送通知
    """

    notify_channels = [
        channels.Desktop,
        channels.PushPlus,
        channels.Bark,
        channels.Gotify,
        channels.DingTalk,
        channels.Email,
        channels.PushMe,
        channels.PushDeer,
        channels.ServerChan,
        channels.Slack,
        channels.Telegram,
        channels.WeComBot,
        channels.DGLab,
    ]

    @staticmethod
    def append(apprise_queue: Apprise, external_queue: deque) -> None:
        """
        添加至队列
        """
        for channel in NotificationManager.notify_channels:
            for method in configer.notification.methods:
                if channel.protocol != method:
                    continue

                # 添加外部渠道
                if channel.external:
                    if issubclass(channel, ExternalNotificationChannel):
                        result = channel.add(external_queue)
                    else:
                        log.error(f"渠道 {method} 类型错误")
                        continue
                # 添加内置渠道
                else:
                    result = channel.add(apprise_queue)

                if result:
                    log.info(f"添加 {method} 渠道成功")
                else:
                    log.error(f"添加 {method} 渠道失败")

    @staticmethod
    def send(apprise_queue: Apprise, external_queue: deque) -> None:
        """
        发送通知
        """
        content = NotificationContent()

        # 推送内置渠道通知
        if len(apprise_queue) > 0:
            result = apprise_queue.notify(
                title=content.title,
                body=content.body,
            )
            if not result:
                raise NotificationError("发送通知失败")

        # 发送外部渠道通知
        while len(external_queue) > 0:
            method = external_queue.popleft()
            for channel in NotificationManager.notify_channels:
                if channel.protocol == method:
                    if issubclass(channel, ExternalNotificationChannel):
                        channel.send(content)

    @staticmethod
    def push() -> None:
        """
        推送通知
        """
        if not configer.notification.isEnable:
            return

        if not configer.notification.methods:
            log.warning("未启用任何通知方式")
            return

        apprise_queue = Apprise()
        external_queue = deque()

        try:
            NotificationManager.append(apprise_queue, external_queue)
            NotificationManager.send(apprise_queue, external_queue)
        except NotificationError as e:
            log.error(f"推送通知失败: {e}")

    @staticmethod
    def init_external() -> None:
        """
        初始化外部通知
        """
        for channel in NotificationManager.notify_channels:
            if not channel.external:
                continue
            if not issubclass(channel, ExternalNotificationChannel):
                continue
            if channel.protocol not in configer.notification.methods:
                continue
            try:
                channel.init()
                log.info(f"初始化 {channel.protocol} 外部渠道成功")
            except Exception as e:
                log.error(f"初始化 {channel.protocol} 外部渠道失败: {e}")

    @staticmethod
    def start_external() -> None:
        """
        启动外部通知服务
        """
        for channel in NotificationManager.notify_channels:
            if not channel.external:
                continue
            if not issubclass(channel, ExternalNotificationChannel):
                continue
            if channel.protocol not in configer.notification.methods:
                continue
            try:
                channel.start()
                log.info(f"启动 {channel.protocol} 外部渠道成功")
            except Exception as e:
                log.error(f"启动 {channel.protocol} 外部渠道失败: {e}")

    @staticmethod
    def connect_external() -> None:
        """
        等待外部通知服务连接
        """
        for channel in NotificationManager.notify_channels:
            if not channel.external:
                continue
            if not issubclass(channel, ExternalNotificationChannel):
                continue
            if channel.protocol not in configer.notification.methods:
                continue
            try:
                channel.connect()
                log.info(f"连接 {channel.protocol} 外部渠道成功")
            except Exception as e:
                log.error(f"连接 {channel.protocol} 外部渠道失败: {e}")

    @staticmethod
    def stop_external() -> None:
        """
        停止外部服务
        """
        for channel in NotificationManager.notify_channels:
            if not channel.external:
                continue
            if not issubclass(channel, ExternalNotificationChannel):
                continue
            if channel.protocol not in configer.notification.methods:
                continue
            try:
                channel.stop()
                log.info(f"停止 {channel.protocol} 外部渠道成功")
            except Exception as e:
                log.error(f"停止 {channel.protocol} 外部渠道失败: {e}")
