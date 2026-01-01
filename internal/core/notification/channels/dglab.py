from collections import deque

from internal.config import configer
from internal.core.notification import NotificationContent
from internal.core.notification.channels.base import ExternalNotificationChannel
from internal.core.notification.external.dglab import dglab_manager
from internal.error import NotificationError


class DGLab(ExternalNotificationChannel):
    """
    DGLab 通知
    """

    protocol = "dglab"

    @classmethod
    def add(cls, queue: deque) -> bool:
        """
        添加至队列

        :return bool: 添加成功与否
        """
        if cls.protocol not in configer.notification.methods:
            return False

        queue.append(cls.protocol)

        return True

    @classmethod
    def init(cls) -> None:
        """
        初始化服务
        """
        dglab_manager.init()

    @classmethod
    def start(cls) -> None:
        """
        启动服务
        """
        dglab_manager.start()

    @classmethod
    def connect(cls) -> None:
        """
        等待连接
        """
        dglab_manager.connect()

    @classmethod
    def stop(cls) -> None:
        """
        停止服务
        """
        dglab_manager.stop()

    @classmethod
    def status(cls) -> bool:
        """
        服务状态

        :return bool: 状态值
        """
        return dglab_manager.status()

    @classmethod
    def send(cls, notice: NotificationContent) -> None:
        """
        发送 DGLab 通知
        """
        if cls.protocol not in configer.notification.methods:
            return

        if not dglab_manager.status():
            dglab_manager.start()
            dglab_manager.connect()

        if not dglab_manager.status():
            raise NotificationError("DGLab 客户端未连接，无法发送通知")

        config = configer.notification.dglab
        pulses = config.pulses
        strength = config.strength
        channel_str = config.channel
        interval = config.interval

        try:
            dglab_manager.send_notification(pulses, strength, channel_str, interval)
        except ValueError as e:
            raise NotificationError(str(e))
        except Exception as e:
            raise NotificationError(f"发送 DGLab 通知失败: {e}")
