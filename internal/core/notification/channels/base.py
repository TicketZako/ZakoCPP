from abc import ABC, abstractmethod
from collections import deque
from typing import ClassVar

from apprise import Apprise

from internal.core.notification import NotificationContent


class BaseNotificationChannel(ABC):
    """
    通知渠道基类
    """

    protocol: ClassVar[str] = ""
    external: ClassVar[bool] = False

    @classmethod
    @abstractmethod
    def add(cls, *args, **kwargs) -> bool:
        """
        添加渠道

        :return bool: 添加成功与否
        """
        pass


class AppriseNotificationChannel(BaseNotificationChannel):
    """
    内置通知渠道基类（基于Apprise）
    """

    external: ClassVar[bool] = False

    @classmethod
    @abstractmethod
    def add(cls, queue: Apprise) -> bool:
        """
        添加至队列

        :param queue: Apprise实例

        :return bool: 添加成功与否
        """
        pass


class ExternalNotificationChannel(BaseNotificationChannel):
    """
    外部通知渠道基类
    """

    external: ClassVar[bool] = True

    @classmethod
    @abstractmethod
    def add(cls, queue: deque) -> bool:
        """
        添加渠道

        :return bool: 添加成功与否
        """
        pass

    @classmethod
    @abstractmethod
    def send(cls, notice: NotificationContent) -> None:
        """
        发送通知
        """
        pass

    @classmethod
    @abstractmethod
    def init(cls) -> None:
        """
        初始化服务
        """
        pass

    @classmethod
    @abstractmethod
    def start(cls) -> None:
        """
        启动服务
        """
        pass

    @classmethod
    @abstractmethod
    def connect(cls) -> None:
        """
        等待连接
        """

    @classmethod
    @abstractmethod
    def stop(cls) -> None:
        """
        停止服务
        """

    @classmethod
    @abstractmethod
    def status(cls) -> bool:
        """
        服务状态

        :return bool: 状态值
        """
        pass
