from internal.config import configer
from internal.core.notification import NotificationManager
from internal.core.notification.channels.base import ExternalNotificationChannel
from internal.core.service import UserService
from internal.error import LoginStatusCode
from internal.interface.cli.menu.notification import CliNotification
from internal.interface.cli.menu.user import CliLogin
from internal.util import CliUtils, log


class CliInit:
    """
    CLI 初始化模块
    """

    @staticmethod
    def init_account() -> None:
        """
        初始化账户
        """
        log.info("账户初始化中...")
        if not configer.account.account or not configer.account.password:
            log.warn("未登录 CPP，请先登录！")
            CliLogin.generate()
        else:
            if UserService.login() != LoginStatusCode.Success:
                log.warn("账户失效，重新登录！")
                CliLogin.generate()
        log.info("账户初始化完成")

    @staticmethod
    def _get_external_channel_display_names(protocols: list[str]) -> list[str]:
        """
        获取外部渠道的显示名称列表

        :param protocols: 渠道协议名称列表
        :return: 显示名称列表
        """
        return [
            CliNotification.METHOD_NAMES.get(protocol, protocol)
            for protocol in protocols
        ]

    @staticmethod
    def _get_configured_external_channels() -> list[str]:
        """
        获取已配置的外部通知渠道列表

        :return: 外部渠道协议名称列表
        """
        external_channels = []
        for channel in NotificationManager.notify_channels:
            if not channel.external:
                continue
            if not issubclass(channel, ExternalNotificationChannel):
                continue
            if channel.protocol in configer.notification.methods:
                external_channels.append(channel.protocol)
        return external_channels

    @staticmethod
    def _ask_user_to_start_external(protocol: str) -> bool:
        """
        询问用户是否启动单个外部服务

        :param protocol: 外部渠道协议名称
        :return: 用户是否选择启动
        """
        display_name = CliNotification.METHOD_NAMES.get(protocol, protocol)

        CliUtils.print("", end="\n")
        CliUtils.print(
            f"检测到已配置的外部通知服务: {display_name}",
            color="yellow",
            bold=True,
        )
        CliUtils.print("", end="\n")

        result = CliUtils.inquire(
            type="Confirm",
            message=f"是否启动并连接 {display_name} 外部通知服务？",
            default=True,
        )
        return bool(result)

    @staticmethod
    def _remove_external_channels(protocols: list[str]) -> None:
        """
        从配置中移除外部通知渠道

        :param protocols: 要移除的渠道协议名称列表
        """
        for protocol in protocols:
            if protocol in configer.notification.methods:
                configer.notification.methods.remove(protocol)
                log.info(f"已从配置中移除 {protocol} 外部渠道")

    @staticmethod
    def init_external_notification() -> None:
        """
        初始化外部通知服务
        """
        NotificationManager.init_external()

        external_channels = CliInit._get_configured_external_channels()

        if not external_channels:
            return

        channels_to_remove = []

        for protocol in external_channels:
            display_name = CliNotification.METHOD_NAMES.get(protocol, protocol)
            should_start = CliInit._ask_user_to_start_external(protocol)

            if should_start:
                for channel in NotificationManager.notify_channels:
                    if (
                        channel.external
                        and issubclass(channel, ExternalNotificationChannel)
                        and channel.protocol == protocol
                    ):
                        try:
                            channel.start()
                            channel.connect()
                            log.info(f"启动 {protocol} 外部渠道成功")
                        except Exception as e:
                            log.error(f"启动 {protocol} 外部渠道失败: {e}")
                        break
            else:
                channels_to_remove.append(protocol)
                CliUtils.print("", end="\n")
                CliUtils.print(
                    f"已跳过 {display_name} 外部通知服务",
                    color="yellow",
                )

        if channels_to_remove:
            CliInit._remove_external_channels(channels_to_remove)
            display_names = CliInit._get_external_channel_display_names(
                channels_to_remove
            )
            channels_text = "、".join(display_names)
            log.info(f"用户选择不启动的外部通知服务，已从配置中移除: {channels_text}")

    @staticmethod
    def init() -> None:
        """
        执行所有初始化操作
        """

        # 初始化账户
        CliInit.init_account()

        # 初始化外部通知服务
        CliInit.init_external_notification()
