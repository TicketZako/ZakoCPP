from functools import partial
from typing import ClassVar, List

from internal.config import configer
from internal.core.notification import NotificationManager
from internal.core.notification.external.dglab.pulse import PULSE_DATA
from internal.util import CliUtils, log


class CliNotification:
    """
    通知配置主界面
    """

    METHOD_NAMES: ClassVar[dict[str, str]] = {
        "desktop": "Desktop",
        "pushplus": "PushPlus",
        "bark": "Bark",
        "gotify": "Gotify",
        "dingtalk": "DingTalk",
        "mailto": "Email",
        "pushme": "PushMe",
        "pushdeer": "PushDeer",
        "schan": "ServerChan",
        "slack": "Slack",
        "tgram": "Telegram",
        "wecombot": "WeComBot",
        "dglab": "DGLab",
    }

    @staticmethod
    def _get_status_text() -> str:
        """
        获取当前通知状态文本

        :return: 状态文本
        """
        if not configer.notification.isEnable:
            return "关闭"
        methods = configer.notification.methods
        if not methods:
            return "开启（未配置渠道）"
        return f"开启（{', '.join([CliNotification.METHOD_NAMES.get(m, m) for m in methods])}）"

    @staticmethod
    def _get_channel_status(method: str) -> str:
        """
        获取渠道配置状态

        :param method: 渠道名称
        :return: 状态文本
        """
        name = CliNotification.METHOD_NAMES.get(method, method)

        if method == "desktop":
            if method not in configer.notification.methods:
                return f"{name}（未配置）"
            return f"{name}（已配置）"

        elif method == "pushplus":
            if configer.notification.pushplus.token:
                return f"{name}（已配置）"
            return f"{name}（未配置）"

        elif method == "bark":
            if configer.notification.bark.token:
                bark_level = CliBark.LEVEL_NAMES.get(
                    configer.notification.bark.level, "静默通知"
                )
                return f"{name}（已配置，等级：{bark_level}）"
            return f"{name}（未配置）"

        elif method == "dingtalk":
            if configer.notification.dingtalk.token:
                return f"{name}（已配置）"
            return f"{name}（未配置）"

        elif method == "gotify":
            if configer.notification.gotify.token and configer.notification.gotify.host:
                return f"{name}（已配置）"
            return f"{name}（未配置）"

        elif method == "mailto":
            if (
                configer.notification.email.smtp_host
                and configer.notification.email.smtp_user
                and configer.notification.email.smtp_pass
                and configer.notification.email.to_addr
            ):
                return f"{name}（已配置）"
            return f"{name}（未配置）"

        elif method == "pushme":
            if configer.notification.pushme.token:
                return f"{name}（已配置）"
            return f"{name}（未配置）"

        elif method == "pushdeer":
            if configer.notification.pushdeer.push_key:
                return f"{name}（已配置）"
            return f"{name}（未配置）"

        elif method == "schan":
            if configer.notification.serverchan.token:
                return f"{name}（已配置）"
            return f"{name}（未配置）"

        elif method == "slack":
            if configer.notification.slack.oauth_token:
                return f"{name}（已配置，OAuth 方式）"
            elif (
                configer.notification.slack.token_a
                and configer.notification.slack.token_b
                and configer.notification.slack.token_c
            ):
                return f"{name}（已配置，Webhook 方式）"
            return f"{name}（未配置）"

        elif method == "tgram":
            if (
                configer.notification.telegram.bot_token
                and configer.notification.telegram.chat_id
            ):
                return f"{name}（已配置）"
            return f"{name}（未配置）"

        elif method == "wecombot":
            if configer.notification.wecombot.bot_key:
                return f"{name}（已配置）"
            return f"{name}（未配置）"

        elif method == "dglab":
            if method not in configer.notification.methods:
                return f"{name}（未配置）"
            pulses = configer.notification.dglab.pulses
            strength = configer.notification.dglab.strength
            channel = configer.notification.dglab.channel
            pulse_str = ", ".join(pulses) if pulses else "无"
            return f"{name}（已配置，波形：{pulse_str}，强度：{strength}，通道：{channel}）"

        return name

    @staticmethod
    def _toggle_enable():
        """
        切换通知启用状态
        """
        configer.notification.isEnable = not configer.notification.isEnable
        if configer.notification.isEnable:
            log.info("通知功能已开启")
        else:
            log.info("通知功能已关闭")
            # 关闭时清空通知方式（重新赋值以触发自动保存）
            configer.notification.methods = []

    @staticmethod
    def _toggle_channel(method: str):
        """
        切换渠道启用状态

        :param method: 渠道名称
        """
        if method not in configer.notification.methods:
            configer.notification.methods.append(method)
            log.info(f"{method} 渠道已启用")
        else:
            configer.notification.methods.remove(method)
            log.info(f"{method} 渠道已禁用")

    @staticmethod
    def _append_menu_item(items: list, channel: str):
        """
        添加菜单项列表频道

        :param items: 菜单项列表
        :param channel: 渠道名称
        """
        status = CliNotification._get_channel_status(channel)
        is_enabled = channel in configer.notification.methods
        prefix = "✓ " if is_enabled else "  "
        description = CliNotification.METHOD_NAMES.get(channel, channel)
        items.append(
            {
                "name": f"{prefix}{status}",
                "target": partial(CliNotification._handle_channel, channel),
                "description": f"配置 {description} 渠道",
            }
        )
        return items

    @staticmethod
    def _build_menu_items() -> list:
        """
        构建菜单项列表

        :return: 菜单项列表
        """
        items = []

        status_text = CliNotification._get_status_text()
        items.append(
            {
                "name": f"通知状态: {status_text}",
                "target": CliNotification._toggle_enable,
                "description": "切换通知开关",
            }
        )

        if not configer.notification.isEnable:
            return items

        for channel in CliNotification.METHOD_NAMES.keys():
            items = CliNotification._append_menu_item(items, channel)

        return items

    @staticmethod
    def _handle_channel(method: str):
        """
        处理渠道配置

        :param method: 渠道名称
        """
        if method not in configer.notification.methods:
            configer.notification.methods.append(method)

        if method == "desktop":
            pass
        elif method == "pushplus":
            CliPushPlus.generate()
        elif method == "bark":
            CliBark.generate()
        elif method == "dingtalk":
            CliDingTalk.generate()
        elif method == "gotify":
            CliGotify.generate()
        elif method == "mailto":
            CliEmail.generate()
        elif method == "pushme":
            CliPushme.generate()
        elif method == "pushdeer":
            CliPushdeer.generate()
        elif method == "schan":
            CliServerchan.generate()
        elif method == "slack":
            CliSlack.generate()
        elif method == "tgram":
            CliTelegram.generate()
        elif method == "wecombot":
            CliWecombot.generate()
        elif method == "dglab":
            CliDglab.generate()

    @staticmethod
    def generate():
        """
        通知配置窗口
        """
        while True:
            items = CliNotification._build_menu_items()

            # 构建菜单选择项
            choices = []
            menu_map = {}

            for item in items:
                name = item.get("name", "未命名")
                description = item.get("description", "")
                if description:
                    display_name = f"{name} - {description}"
                else:
                    display_name = name
                choices.append(display_name)
                menu_map[display_name] = item.get("target")

            choices.append("返回")
            menu_map["返回"] = "back"

            # 显示菜单标题
            CliUtils.print("", end="\n")
            CliUtils.print("通知配置", color="cyan", size="large")
            CliUtils.print("", end="\n")

            # 选择菜单项
            selected = CliUtils.inquire(
                type="List",
                message="请选择操作",
                choices=choices,
            )

            if selected == "返回":
                NotificationManager.start_external()
                NotificationManager.connect_external()
                break

            target = menu_map.get(selected)

            if target is None:
                log.error(f"未找到菜单项 '{selected}' 的目标")
                continue

            try:
                if callable(target):
                    target()
                CliUtils.print("", end="\n")
            except Exception as e:
                log.error(f"执行菜单项 '{selected}' 时出错: {e}")
                CliUtils.print("", end="\n")
                continue


class CliPushPlus:
    """
    PushPlus 通知配置
    """

    @staticmethod
    def generate():
        """
        PushPlus 配置窗口
        """
        CliUtils.print("", end="\n")
        CliUtils.print("PushPlus 配置", color="blue", size="large", style="underline")
        CliUtils.print("", end="\n")

        while True:
            token = CliUtils.inquire(
                type="Text",
                message="请输入 PushPlus Token",
                default="",
            )

            if not token:
                CliUtils.print("Token 不能为空", color="red")
                retry = CliUtils.inquire(
                    type="Confirm",
                    message="是否重新输入？",
                    default=True,
                )
                if not retry:
                    return
                continue

            configer.notification.pushplus.token = token
            CliUtils.print("", end="\n")
            CliUtils.print("✅ PushPlus Token 已配置", color="green")
            log.info("PushPlus Token 已配置")
            break


class CliBark:
    """
    Bark 通知配置
    """

    LEVEL_NAMES: ClassVar[dict[str, str]] = {
        "passive": "静默通知",
        "timeSensitive": "时效性通知",
        "active": "亮屏通知",
        "critical": "重要通知",
    }

    @staticmethod
    def generate():
        """
        Bark 配置窗口
        """
        CliUtils.print("", end="\n")
        CliUtils.print("Bark 配置", color="blue", size="large", style="underline")
        CliUtils.print("", end="\n")

        # 输入 Token
        while True:
            token = CliUtils.inquire(
                type="Text",
                message="请输入 Bark Token",
                default="",
            )

            if not token:
                CliUtils.print("Token 不能为空", color="red")
                retry = CliUtils.inquire(
                    type="Confirm",
                    message="是否重新输入？",
                    default=True,
                )
                if not retry:
                    return
                continue

            configer.notification.bark.token = token
            break

        # 选择通知等级
        CliUtils.print("", end="\n")
        selected_level = CliUtils.inquire(
            type="List",
            message="请选择通知等级",
            choices=list(CliBark.LEVEL_NAMES.values()),
            default=CliBark.LEVEL_NAMES.get(
                configer.notification.bark.level, "静默通知"
            ),
        )

        # 将选择转换回配置值
        for level, name in CliBark.LEVEL_NAMES.items():
            if name == selected_level:
                configer.notification.bark.level = level
                break

        CliUtils.print("", end="\n")
        CliUtils.print("✅ Bark 配置完成", color="green")
        log.info(f"Bark 配置完成，通知等级: {selected_level}")


class CliGotify:
    """
    Gotify 配置
    """

    @staticmethod
    def generate():
        """
        Gotify 配置窗口
        """
        CliUtils.print("", end="\n")
        CliUtils.print("Gotify 配置", color="blue", size="large", style="underline")
        CliUtils.print("", end="\n")

        # 输入 Host
        while True:
            host = CliUtils.inquire(
                type="Text",
                message="请输入 Gotify Host",
                default="",
            )

            if not host:
                CliUtils.print("Host 不能为空", color="red")
                retry = CliUtils.inquire(
                    type="Confirm",
                    message="是否重新输入？",
                    default=True,
                )
                if not retry:
                    return
                continue

            configer.notification.gotify.host = host
            break

        # 输入 Token
        while True:
            token = CliUtils.inquire(
                type="Text",
                message="请输入 Gotify Token",
                default="",
            )

            if not token:
                CliUtils.print("Token 不能为空", color="red")
                retry = CliUtils.inquire(
                    type="Confirm",
                    message="是否重新输入？",
                    default=True,
                )
                if not retry:
                    return
                continue

            configer.notification.gotify.token = token
            break

        # 输入自定义服务器地址（可选）
        host = CliUtils.inquire(
            type="Text",
            message="请输入 PushDeer 服务器地址（可选，留空使用默认服务）",
            default=configer.notification.gotify.host or "",
        )
        if host:
            configer.notification.gotify.host = host

            # 输入端口（可选）
            port = CliUtils.inquire(
                type="Text",
                message="请输入 PushDeer 服务器端口（可选）",
                default=str(configer.notification.gotify.port)
                if configer.notification.gotify.port
                else "",
            )
            if port:
                try:
                    configer.notification.gotify.port = int(port)
                except ValueError:
                    CliUtils.print("端口必须是数字，将忽略此设置", color="yellow")
                    configer.notification.gotify.port = None
            else:
                configer.notification.gotify.port = None
        else:
            configer.notification.gotify.host = None
            configer.notification.gotify.port = None

        # 选择是否使用 SSL/TLS
        use_tls = CliUtils.inquire(
            type="Confirm",
            message="是否使用 SSL/TLS？",
            default=configer.notification.pushdeer.use_tls,
        )
        configer.notification.gotify.use_tls = use_tls

        CliUtils.print("", end="\n")
        CliUtils.print("✅ Gotify 配置完成", color="green")
        log.info("Gotify 配置完成")


class CliDingTalk:
    """
    DingTalk 通知配置
    """

    @staticmethod
    def generate():
        """
        DingTalk 配置窗口
        """
        CliUtils.print("", end="\n")
        CliUtils.print("DingTalk 配置", color="blue", size="large", style="underline")
        CliUtils.print("", end="\n")

        # 输入 Token
        while True:
            token = CliUtils.inquire(
                type="Text",
                message="请输入 DingTalk Token",
                default="",
            )

            if not token:
                CliUtils.print("Token 不能为空", color="red")
                retry = CliUtils.inquire(
                    type="Confirm",
                    message="是否重新输入？",
                    default=True,
                )
                if not retry:
                    return
                continue

            configer.notification.dingtalk.token = token
            break

        CliUtils.print("", end="\n")
        CliUtils.print("✅ DingTalk 配置完成", color="green")
        log.info("DingTalk 配置完成")


class CliEmail:
    """
    Email 通知配置
    """

    @staticmethod
    def generate():
        """
        Email 配置窗口
        """
        CliUtils.print("", end="\n")
        CliUtils.print("Email 配置", color="blue", size="large", style="underline")
        CliUtils.print("", end="\n")

        # 输入 SMTP 服务器地址
        while True:
            smtp_host = CliUtils.inquire(
                type="Text",
                message="请输入 SMTP 服务器地址",
                default=configer.notification.email.smtp_host or "",
            )

            if not smtp_host:
                CliUtils.print("SMTP 服务器地址不能为空", color="red")
                retry = CliUtils.inquire(
                    type="Confirm",
                    message="是否重新输入？",
                    default=True,
                )
                if not retry:
                    return
                continue

            configer.notification.email.smtp_host = smtp_host
            break

        # 输入 SMTP 端口
        smtp_port = CliUtils.inquire(
            type="Text",
            message="请输入 SMTP 端口",
            default=str(configer.notification.email.smtp_port or 587),
        )
        try:
            configer.notification.email.smtp_port = int(smtp_port)
        except ValueError:
            CliUtils.print("端口必须是数字，使用默认值 587", color="yellow")
            configer.notification.email.smtp_port = 587

        # 输入 SMTP 用户名
        while True:
            smtp_user = CliUtils.inquire(
                type="Text",
                message="请输入 SMTP 用户名（邮箱地址）",
                default=configer.notification.email.smtp_user or "",
            )

            if not smtp_user:
                CliUtils.print("SMTP 用户名不能为空", color="red")
                retry = CliUtils.inquire(
                    type="Confirm",
                    message="是否重新输入？",
                    default=True,
                )
                if not retry:
                    return
                continue

            configer.notification.email.smtp_user = smtp_user
            break

        # 输入 SMTP 密码
        while True:
            smtp_pass = CliUtils.inquire(
                type="Password",
                message="请输入 SMTP 密码",
                default="",
            )

            if not smtp_pass:
                CliUtils.print("SMTP 密码不能为空", color="red")
                retry = CliUtils.inquire(
                    type="Confirm",
                    message="是否重新输入？",
                    default=True,
                )
                if not retry:
                    return
                continue

            configer.notification.email.smtp_pass = smtp_pass
            break

        # 选择是否使用 TLS
        use_tls = CliUtils.inquire(
            type="Confirm",
            message="是否使用 TLS/SSL？",
            default=configer.notification.email.use_tls,
        )
        configer.notification.email.use_tls = use_tls

        # 输入发件人邮箱（可选）
        from_addr = CliUtils.inquire(
            type="Text",
            message="请输入发件人邮箱地址（可选，留空则使用 SMTP 用户名）",
            default=configer.notification.email.from_addr or "",
        )
        if from_addr:
            configer.notification.email.from_addr = from_addr
        else:
            configer.notification.email.from_addr = (
                configer.notification.email.smtp_user
            )

        # 输入收件人邮箱
        while True:
            to_input = CliUtils.inquire(
                type="Text",
                message="请输入收件人邮箱地址（多个用逗号分隔）",
                default=(
                    ",".join(configer.notification.email.to_addr)
                    if isinstance(configer.notification.email.to_addr, list)
                    else (configer.notification.email.to_addr or "")
                ),
            )

            if not to_input:
                CliUtils.print("收件人邮箱地址不能为空", color="red")
                retry = CliUtils.inquire(
                    type="Confirm",
                    message="是否重新输入？",
                    default=True,
                )
                if not retry:
                    return
                continue

            # 处理多个收件人
            to_list = [email.strip() for email in to_input.split(",") if email.strip()]
            if len(to_list) == 1:
                configer.notification.email.to_addr = to_list[0]
            else:
                configer.notification.email.to_addr = to_list
            break

        CliUtils.print("", end="\n")
        CliUtils.print("✅ Email 配置完成", color="green")
        log.info("Email 配置完成")


class CliPushme:
    """
    PushMe 通知配置
    """

    @staticmethod
    def generate():
        """
        PushMe 配置窗口
        """
        CliUtils.print("", end="\n")
        CliUtils.print("PushMe 配置", color="blue", size="large", style="underline")
        CliUtils.print("", end="\n")

        # 输入 Token
        while True:
            token = CliUtils.inquire(
                type="Text",
                message="请输入 PushMe Token",
                default=configer.notification.pushme.token or "",
            )

            if not token:
                CliUtils.print("Token 不能为空", color="red")
                retry = CliUtils.inquire(
                    type="Confirm",
                    message="是否重新输入？",
                    default=True,
                )
                if not retry:
                    return
                continue

            configer.notification.pushme.token = token
            CliUtils.print("", end="\n")
            CliUtils.print("✅ PushMe Token 已配置", color="green")
            log.info("PushMe Token 已配置")
            break


class CliPushdeer:
    """
    PushDeer 通知配置
    """

    @staticmethod
    def generate():
        """
        PushDeer 配置窗口
        """
        CliUtils.print("", end="\n")
        CliUtils.print("PushDeer 配置", color="blue", size="large", style="underline")
        CliUtils.print("", end="\n")

        # 输入 Push Key
        while True:
            push_key = CliUtils.inquire(
                type="Text",
                message="请输入 PushDeer Push Key",
                default=configer.notification.pushdeer.push_key or "",
            )

            if not push_key:
                CliUtils.print("Push Key 不能为空", color="red")
                retry = CliUtils.inquire(
                    type="Confirm",
                    message="是否重新输入？",
                    default=True,
                )
                if not retry:
                    return
                continue

            configer.notification.pushdeer.push_key = push_key
            break

        # 输入自定义服务器地址（可选）
        host = CliUtils.inquire(
            type="Text",
            message="请输入 PushDeer 服务器地址（可选，留空使用默认服务）",
            default=configer.notification.pushdeer.host or "",
        )
        if host:
            configer.notification.pushdeer.host = host

            # 输入端口（可选）
            port = CliUtils.inquire(
                type="Text",
                message="请输入 PushDeer 服务器端口（可选）",
                default=str(configer.notification.pushdeer.port)
                if configer.notification.pushdeer.port
                else "",
            )
            if port:
                try:
                    configer.notification.pushdeer.port = int(port)
                except ValueError:
                    CliUtils.print("端口必须是数字，将忽略此设置", color="yellow")
                    configer.notification.pushdeer.port = None
            else:
                configer.notification.pushdeer.port = None
        else:
            configer.notification.pushdeer.host = None
            configer.notification.pushdeer.port = None

        # 选择是否使用 SSL/TLS
        use_tls = CliUtils.inquire(
            type="Confirm",
            message="是否使用 SSL/TLS？",
            default=configer.notification.pushdeer.use_tls,
        )
        configer.notification.pushdeer.use_tls = use_tls

        CliUtils.print("", end="\n")
        CliUtils.print("✅ PushDeer 配置完成", color="green")
        log.info("PushDeer 配置完成")


class CliServerchan:
    """
    ServerChan 通知配置
    """

    @staticmethod
    def generate():
        """
        ServerChan 配置窗口
        """
        CliUtils.print("", end="\n")
        CliUtils.print("ServerChan 配置", color="blue", size="large", style="underline")
        CliUtils.print("", end="\n")

        # 输入 Token
        while True:
            token = CliUtils.inquire(
                type="Text",
                message="请输入 ServerChan Token",
                default=configer.notification.serverchan.token or "",
            )

            if not token:
                CliUtils.print("Token 不能为空", color="red")
                retry = CliUtils.inquire(
                    type="Confirm",
                    message="是否重新输入？",
                    default=True,
                )
                if not retry:
                    return
                continue

            configer.notification.serverchan.token = token
            CliUtils.print("", end="\n")
            CliUtils.print("✅ ServerChan Token 已配置", color="green")
            log.info("ServerChan Token 已配置")
            break


class CliTelegram:
    """
    Telegram 通知配置
    """

    @staticmethod
    def generate():
        """
        Telegram 配置窗口
        """
        CliUtils.print("", end="\n")
        CliUtils.print("Telegram 配置", color="blue", size="large", style="underline")
        CliUtils.print("", end="\n")

        # 输入 Bot Token
        while True:
            bot_token = CliUtils.inquire(
                type="Text",
                message="请输入 Telegram Bot Token",
                default=configer.notification.telegram.bot_token or "",
            )

            if not bot_token:
                CliUtils.print("Bot Token 不能为空", color="red")
                retry = CliUtils.inquire(
                    type="Confirm",
                    message="是否重新输入？",
                    default=True,
                )
                if not retry:
                    return
                continue

            configer.notification.telegram.bot_token = bot_token
            break

        # 输入 Chat ID
        while True:
            chat_id = CliUtils.inquire(
                type="Text",
                message="请输入 Telegram Chat ID",
                default=configer.notification.telegram.chat_id or "",
            )

            if not chat_id:
                CliUtils.print("Chat ID 不能为空", color="red")
                retry = CliUtils.inquire(
                    type="Confirm",
                    message="是否重新输入？",
                    default=True,
                )
                if not retry:
                    return
                continue

            configer.notification.telegram.chat_id = chat_id
            break

        CliUtils.print("", end="\n")
        CliUtils.print("✅ Telegram 配置完成", color="green")
        log.info("Telegram 配置完成")


class CliSlack:
    """
    Slack 通知配置
    """

    @staticmethod
    def generate():
        """
        Slack 配置窗口
        """
        CliUtils.print("", end="\n")
        CliUtils.print("Slack 配置", color="blue", size="large", style="underline")
        CliUtils.print("", end="\n")

        # 选择配置方式
        CliUtils.print("", end="\n")
        config_type = CliUtils.inquire(
            type="List",
            message="请选择配置方式",
            choices=["Webhook 方式（三个 Token）", "OAuth 方式（一个 Token）"],
        )

        # Webhook 方式配置
        if config_type == "Webhook 方式（三个 Token）":
            # 输入 Token A
            while True:
                token_a = CliUtils.inquire(
                    type="Text",
                    message="请输入 Slack Webhook Token A",
                    default=configer.notification.slack.token_a or "",
                )

                if not token_a:
                    CliUtils.print("Token A 不能为空", color="red")
                    retry = CliUtils.inquire(
                        type="Confirm",
                        message="是否重新输入？",
                        default=True,
                    )
                    if not retry:
                        return
                    continue

                configer.notification.slack.token_a = token_a
                break

            # 输入 Token B
            while True:
                token_b = CliUtils.inquire(
                    type="Text",
                    message="请输入 Slack Webhook Token B",
                    default=configer.notification.slack.token_b or "",
                )

                if not token_b:
                    CliUtils.print("Token B 不能为空", color="red")
                    retry = CliUtils.inquire(
                        type="Confirm",
                        message="是否重新输入？",
                        default=True,
                    )
                    if not retry:
                        return
                    continue

                configer.notification.slack.token_b = token_b
                break

            # 输入 Token C
            while True:
                token_c = CliUtils.inquire(
                    type="Text",
                    message="请输入 Slack Webhook Token C",
                    default=configer.notification.slack.token_c or "",
                )

                if not token_c:
                    CliUtils.print("Token C 不能为空", color="red")
                    retry = CliUtils.inquire(
                        type="Confirm",
                        message="是否重新输入？",
                        default=True,
                    )
                    if not retry:
                        return
                    continue

                configer.notification.slack.token_c = token_c
                # 清空 OAuth token
                configer.notification.slack.oauth_token = ""
                break

        # OAuth 方式配置
        else:
            # 输入 OAuth Token
            while True:
                oauth_token = CliUtils.inquire(
                    type="Text",
                    message="请输入 Slack OAuth Token",
                    default=configer.notification.slack.oauth_token or "",
                )

                if not oauth_token:
                    CliUtils.print("OAuth Token 不能为空", color="red")
                    retry = CliUtils.inquire(
                        type="Confirm",
                        message="是否重新输入？",
                        default=True,
                    )
                    if not retry:
                        return
                    continue

                configer.notification.slack.oauth_token = oauth_token
                # 清空 Webhook tokens
                configer.notification.slack.token_a = ""
                configer.notification.slack.token_b = ""
                configer.notification.slack.token_c = ""
                break

        CliUtils.print("", end="\n")
        CliUtils.print("✅ Slack 配置完成", color="green")
        log.info("Slack 配置完成")


class CliWecombot:
    """
    WeCom Bot 通知配置
    """

    @staticmethod
    def generate():
        """
        WeCom Bot 配置窗口
        """
        CliUtils.print("", end="\n")
        CliUtils.print("WeCom Bot 配置", color="blue", size="large", style="underline")
        CliUtils.print("", end="\n")

        # 输入 Bot Key
        while True:
            botkey = CliUtils.inquire(
                type="Text",
                message="请输入 WeCom Bot Key（从 Webhook URL 中的 key= 参数获取）",
                default=configer.notification.wecombot.bot_key or "",
            )

            if not botkey:
                CliUtils.print("Bot Key 不能为空", color="red")
                retry = CliUtils.inquire(
                    type="Confirm",
                    message="是否重新输入？",
                    default=True,
                )
                if not retry:
                    return
                continue

            configer.notification.wecombot.bot_key = botkey
            CliUtils.print("", end="\n")
            CliUtils.print("✅ WeCom Bot Key 已配置", color="green")
            log.info("WeCom Bot Key 已配置")
            break


class CliDglab:
    """
    DGLab 通知配置
    """

    PULSE_NAMES: ClassVar[List[str]] = list(PULSE_DATA.keys())

    @staticmethod
    def generate():
        """
        DGLab 配置窗口
        """
        CliUtils.print("", end="\n")
        CliUtils.print("DGLab 配置", color="blue", size="large", style="underline")
        CliUtils.print("", end="\n")

        pulses = []
        current_pulses = configer.notification.dglab.pulses.copy()
        if not current_pulses:
            current_pulses = ["呼吸"]

        CliUtils.print("配置波形列表（按顺序发送）", color="cyan")
        CliUtils.print("当前波形列表:", end=" ")
        if current_pulses:
            CliUtils.print(", ".join(current_pulses), color="yellow")
        else:
            CliUtils.print("无", color="yellow")
        CliUtils.print("", end="\n")

        while True:
            if pulses:
                CliUtils.print(f"已选择波形: {', '.join(pulses)}", color="green")
            else:
                CliUtils.print("已选择波形: 无", color="yellow")

            action = CliUtils.inquire(
                type="List",
                message="请选择操作",
                choices=["添加波形", "移除最后一个波形", "清空列表", "完成配置"],
                default="添加波形" if not pulses else "完成配置",
            )

            if action == "添加波形":
                available_pulses = [w for w in CliDglab.PULSE_NAMES if w not in pulses]
                if not available_pulses:
                    CliUtils.print("所有波形已添加", color="yellow")
                    continue

                selected = CliUtils.inquire(
                    type="List",
                    message="请选择要添加的波形",
                    choices=available_pulses,
                )
                pulses.append(selected)
                CliUtils.print(f"已添加波形: {selected}", color="green")

            elif action == "移除最后一个波形":
                if pulses:
                    removed = pulses.pop()
                    CliUtils.print(f"已移除波形: {removed}", color="yellow")
                else:
                    CliUtils.print("波形列表为空", color="red")

            elif action == "清空列表":
                if pulses:
                    pulses.clear()
                    CliUtils.print("已清空波形列表", color="yellow")
                else:
                    CliUtils.print("波形列表已为空", color="yellow")

            elif action == "完成配置":
                if not pulses:
                    CliUtils.print("波形列表不能为空", color="red")
                    retry = CliUtils.inquire(
                        type="Confirm",
                        message="是否继续配置？",
                        default=True,
                    )
                    if retry:
                        continue
                    else:
                        return
                break

        configer.notification.dglab.pulses = pulses

        while True:
            strength_str = CliUtils.inquire(
                type="Text",
                message="请输入强度（0-100）",
                default=str(configer.notification.dglab.strength),
            )
            try:
                strength = int(strength_str)
                if 0 <= strength <= 100:
                    configer.notification.dglab.strength = strength
                    break
                else:
                    CliUtils.print("强度必须在 0-100 之间", color="red")
                    retry = CliUtils.inquire(
                        type="Confirm",
                        message="是否重新输入？",
                        default=True,
                    )
                    if not retry:
                        return
            except ValueError:
                CliUtils.print("强度必须是数字", color="red")
                retry = CliUtils.inquire(
                    type="Confirm",
                    message="是否重新输入？",
                    default=True,
                )
                if not retry:
                    return

        while True:
            interval_str = CliUtils.inquire(
                type="Text",
                message="请输入波形间隔时间（秒，0-10）",
                default=str(configer.notification.dglab.interval),
            )
            try:
                interval = float(interval_str)
                if 0 <= interval <= 10:
                    configer.notification.dglab.interval = interval
                    break
                else:
                    CliUtils.print("间隔时间必须在 0-10 之间", color="red")
                    retry = CliUtils.inquire(
                        type="Confirm",
                        message="是否重新输入？",
                        default=True,
                    )
                    if not retry:
                        return
            except ValueError:
                CliUtils.print("间隔时间必须是数字", color="red")
                retry = CliUtils.inquire(
                    type="Confirm",
                    message="是否重新输入？",
                    default=True,
                )
                if not retry:
                    return

        selected_channel = CliUtils.inquire(
            type="List",
            message="请选择通道",
            choices=["A", "B"],
            default=configer.notification.dglab.channel,
        )
        configer.notification.dglab.channel = selected_channel

        CliUtils.print("", end="\n")
        CliUtils.print("✅ DGLab 配置完成", color="green")
        log.info(
            f"DGLab 配置完成，波形：{', '.join(pulses)}，强度：{configer.notification.dglab.strength}，间隔：{configer.notification.dglab.interval}秒，通道：{selected_channel}"
        )
