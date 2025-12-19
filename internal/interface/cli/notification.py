from functools import partial

from internal.config import configer
from internal.util import CliUtils, log


class CliNotification:
    """
    通知配置主界面
    """

    METHOD_NAMES = {
        "pushplus": "PushPlus",
        "bark": "Bark",
    }

    @staticmethod
    def _get_status_text() -> str:
        """
        获取当前通知状态文本

        :return: 状态文本
        """
        if not configer.notification.isEnable:
            return "关闭"
        methods = configer.notification.notifyMethod
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

        if method == "pushplus":
            if configer.notification.pushplus.token:
                return f"{name}（已配置）"
            return f"{name}（未配置）"
        if method == "bark":
            if configer.notification.bark.token:
                level = CliBark.LEVEL_NAMES.get(
                    configer.notification.bark.level, "被动"
                )
                return f"{name}（已配置，等级：{level}）"
            return f"{name}（未配置）"
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
            configer.notification.notifyMethod = []

    @staticmethod
    def _toggle_channel(method: str):
        """
        切换渠道启用状态

        :param method: 渠道名称
        """
        if method not in configer.notification.notifyMethod:
            configer.notification.notifyMethod.append(method)
            log.info(f"{method} 渠道已启用")
        else:
            configer.notification.notifyMethod.remove(method)
            log.info(f"{method} 渠道已禁用")

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

        # PushPlus 渠道
        pushplus_status = CliNotification._get_channel_status("pushplus")
        is_pushplus_enabled = "pushplus" in configer.notification.notifyMethod
        pushplus_prefix = "✓ " if is_pushplus_enabled else "  "
        items.append(
            {
                "name": f"{pushplus_prefix}{pushplus_status}",
                "target": partial(CliNotification._handle_channel, "pushplus"),
                "description": "配置 PushPlus 渠道",
            }
        )

        # Bark 渠道
        bark_status = CliNotification._get_channel_status("bark")
        is_bark_enabled = "bark" in configer.notification.notifyMethod
        bark_prefix = "✓ " if is_bark_enabled else "  "
        items.append(
            {
                "name": f"{bark_prefix}{bark_status}",
                "target": partial(CliNotification._handle_channel, "bark"),
                "description": "配置 Bark 渠道",
            }
        )

        return items

    @staticmethod
    def _handle_channel(method: str):
        """
        处理渠道配置

        :param method: 渠道名称
        """
        if method not in configer.notification.notifyMethod:
            configer.notification.notifyMethod.append(method)

        if method == "pushplus":
            CliPushPlus.generate()
        elif method == "bark":
            CliBark.generate()

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

    LEVEL_NAMES = {
        "passive": "被动",
        "timeSensitive": "时效性",
        "active": "主动",
        "critical": "关键",
    }

    LEVEL_FULL_NAMES = {
        "passive": "被动（passive）",
        "timeSensitive": "时效性（timeSensitive）",
        "active": "主动（active）",
        "critical": "关键（critical）",
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
            choices=list(CliBark.LEVEL_FULL_NAMES.values()),
            default=CliBark.LEVEL_FULL_NAMES.get(
                configer.notification.bark.level, "被动（passive）"
            ),
        )

        # 将选择转换回配置值
        for level, name in CliBark.LEVEL_FULL_NAMES.items():
            if name == selected_level:
                configer.notification.bark.level = level
                break

        CliUtils.print("", end="\n")
        CliUtils.print("✅ Bark 配置完成", color="green")
        log.info(f"Bark 配置完成，通知等级: {selected_level}")
