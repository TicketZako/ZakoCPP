from sys import exit
from re import compile
from time import sleep
from typing import Any

from inquirer import Text, Confirm, List, Checkbox, Password, prompt
from inquirer.themes import GreenPassion

from internal.util.system import SystemUtils
from internal.util.logger import log


class CustomThemes(GreenPassion):
    """
    自定义主题
    """

    def __init__(self):
        """
        初始化
        """
        super().__init__()

        # 选择光标
        self.List.selection_cursor = "->"
        # 选择光标
        self.Checkbox.selection_icon = "->"

        # Checkbox选项 的启用图标
        self.Checkbox.selected_icon = "✔"
        # Checkbox选项 的未启用图标
        self.Checkbox.unselected_icon = "✘"
        # Checkbox选项 的选中颜色(紫, 蓝)
        self.Checkbox.selection_color = "\033[1;35;106m"
        # Checkbox选项 的启用颜色(黄)
        self.Checkbox.selected_color = "\033[93m"

        # List选项 的选中颜色(紫, 蓝)
        self.List.selection_color = "\033[1;35;106m"

        # [?] 中 ? 的颜色(黄)
        self.Question.mark_color = "\033[93m"
        # [?] 中 [] 的颜色(蓝)
        self.Question.brackets_color = "\033[96m"


class CliUtils:
    """
    交互工具
    """

    # ANSI 颜色代码映射
    COLORS = {
        # 前景色
        "black": 30,
        "red": 31,
        "green": 32,
        "yellow": 33,
        "blue": 34,
        "magenta": 35,
        "cyan": 36,
        "white": 37,
        "bright_black": 90,
        "bright_red": 91,
        "bright_green": 92,
        "bright_yellow": 93,
        "bright_blue": 94,
        "bright_magenta": 95,
        "bright_cyan": 96,
        "bright_white": 97,
        # 背景色
        "bg_black": 40,
        "bg_red": 41,
        "bg_green": 42,
        "bg_yellow": 43,
        "bg_blue": 44,
        "bg_magenta": 45,
        "bg_cyan": 46,
        "bg_white": 47,
        "bg_bright_black": 100,
        "bg_bright_red": 101,
        "bg_bright_green": 102,
        "bg_bright_yellow": 103,
        "bg_bright_blue": 104,
        "bg_bright_magenta": 105,
        "bg_bright_cyan": 106,
        "bg_bright_white": 107,
    }

    # ANSI 样式代码映射
    STYLES = {
        "bold": 1,  # 粗体
        "dim": 2,  # 暗淡
        "italic": 3,  # 斜体
        "underline": 4,  # 下划线
        "blink": 5,  # 闪烁
        "reverse": 7,  # 反色
        "strikethrough": 9,  # 删除线
    }

    @staticmethod
    def print(
        text: str,
        color: str | None = None,
        bg_color: str | None = None,
        style: str | list[str] | None = None,
        bold: bool = False,
        size: str = "normal",
        end: str = "\n",
    ) -> None:
        """
        输出带颜色和样式的文本提示

        :param text: 要输出的文本
        :param color: 前景色，可选值: black, red, green, yellow, blue, magenta, cyan, white,
            bright_black, bright_red, bright_green, bright_yellow, bright_blue,
            bright_magenta, bright_cyan, bright_white
        :param bg_color: 背景色，可选值: bg_black, bg_red, bg_green, bg_yellow, bg_blue,
            bg_magenta, bg_cyan, bg_white, bg_bright_black, bg_bright_red,
            bg_bright_green, bg_bright_yellow, bg_bright_blue, bg_bright_magenta,
            bg_bright_cyan, bg_bright_white
        :param style: 样式，可选值: bold, dim, italic, underline, blink, reverse, strikethrough
            可以是单个字符串或字符串列表
        :param bold: 是否粗体（快捷方式，等同于 style="bold"）
        :param size: 字体大小样式，可选值: normal, small, large
            - normal: 正常大小
            - small: 使用 dim 样式（视觉上更小）
            - large: 使用 bold 样式并自动使用亮色（视觉上更大更突出）
        :param end: 输出结束符，默认为换行符
        """
        codes = []
        actual_color = color
        actual_bg_color = bg_color

        if size == "large":
            codes.append(CliUtils.STYLES["bold"])
            if color and not color.startswith("bright_") and color != "black":
                bright_color = f"bright_{color}"
                if bright_color in CliUtils.COLORS:
                    actual_color = bright_color
            if (
                bg_color
                and not bg_color.startswith("bg_bright_")
                and bg_color != "bg_black"
            ):
                bright_bg_color = f"bg_bright_{bg_color.replace('bg_', '')}"
                if bright_bg_color in CliUtils.COLORS:
                    actual_bg_color = bright_bg_color
        elif size == "small":
            codes.append(CliUtils.STYLES["dim"])

        if bold:
            codes.append(CliUtils.STYLES["bold"])

        if style:
            if isinstance(style, str):
                style = [style]
            for s in style:
                if s in CliUtils.STYLES:
                    codes.append(CliUtils.STYLES[s])

        if actual_color:
            if actual_color in CliUtils.COLORS:
                codes.append(CliUtils.COLORS[actual_color])
            else:
                log.warning(f"未知的前景色: {actual_color}")

        if actual_bg_color:
            if actual_bg_color in CliUtils.COLORS:
                codes.append(CliUtils.COLORS[actual_bg_color])
            else:
                log.warning(f"未知的背景色: {actual_bg_color}")

        if codes:
            ansi_start = "\033[" + ";".join(map(str, codes)) + "m"
            ansi_end = "\033[0m"
            formatted_text = f"{ansi_start}{text}{ansi_end}"
        else:
            formatted_text = text

        print(formatted_text, end=end)

    @staticmethod
    def inquire(
        type: str = "Text",
        message: str = "",
        choices: list | None = None,
        default: str | list | bool | None = None,
    ) -> str:
        """
        交互

        :param type: 交互类型 Text, Confirm, List, Checkbox
        :param message: 提示信息
        :param default: 默认值 根据type决定类型
        :param choices: 选项
        """
        choice_method = ["List", "Checkbox"]
        method = {
            "Text": Text,
            "Confirm": Confirm,
            "List": List,
            "Checkbox": Checkbox,
            "Password": Password,
        }

        process = method[type]
        res = prompt(
            [
                process(
                    name="res",
                    message=message,
                    default=default,
                    **({"choices": choices} if type in choice_method else {}),
                )
            ],
            theme=CustomThemes(),
        )

        if res is None:
            log.error("【交互】未知错误!")
            log.warning("程序正在准备退出...")
            sleep(5)
            exit(1)

        if type == "Text":
            p = compile(r"\x1b\[[0-9;]*[mHJ]|[\r\n\x7f\x00-\x1f]")
            result = p.sub("", res["res"])
        else:
            result = res["res"]

        return result

    @staticmethod
    def menu(
        title: str | None = None,
        items: list[dict[str, Any]] | None = None,
        show_back: bool = True,
        back_text: str = "返回",
        title_color: str = "cyan",
        title_size: str = "large",
        is_top_level: bool = False,
    ) -> Any:
        """
        菜单选择工具

        :param title: 菜单标题，如果为 None 则不显示标题
        :param items: 菜单项列表，每个菜单项为字典，格式：
            {
               "name": "菜单项名称",
               "target": 类或菜单配置,
               "description": "可选描述"
            }
            - target 可以是：
             * 类（会自动调用其 generate() 方法）
             * 字典（作为子菜单配置，包含 title 和 items）
             * 可调用对象（直接调用）
        :param show_back: 是否显示返回选项
        :param back_text: 返回选项的文本
        :param title_color: 标题颜色
        :param title_size: 标题大小样式
        :param is_top_level: 是否为一级菜单，如果为 True，选择返回时将退出程序

        :return: 如果选择了返回，返回 "back"（一级菜单会直接退出程序）
                 如果选择了菜单项，返回该菜单项执行后的结果
        """
        if items is None:
            items = []

        actual_back_text = "退出程序" if is_top_level else back_text

        if title:
            CliUtils.print("", end="\n")
            CliUtils.print(title, color=title_color, size=title_size)
            CliUtils.print("", end="\n")

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

        if show_back:
            choices.append(actual_back_text)
            menu_map[actual_back_text] = "back"

        if not choices:
            log.warning("菜单没有可用选项")
            return None

        while True:
            selected = CliUtils.inquire(
                type="List",
                message="请选择操作",
                choices=choices,
            )

            if selected == actual_back_text:
                if is_top_level:
                    SystemUtils.exit(0)
                return "back"

            target = menu_map.get(selected)

            if target is None:
                log.error(f"未找到菜单项 '{selected}' 的目标")
                continue

            try:
                if isinstance(target, dict):
                    result = CliUtils.menu(
                        title=target.get("title"),
                        items=target.get("items", []),
                        show_back=target.get("show_back", True),
                        back_text=target.get("back_text", back_text),
                        title_color=target.get("title_color", title_color),
                        title_size=target.get("title_size", title_size),
                        is_top_level=False,
                    )
                    if result == "back":
                        continue
                elif isinstance(target, type):
                    if hasattr(target, "generate"):
                        target.generate()
                    else:
                        log.error(f"类 {target.__name__} 没有 generate() 方法")
                        continue
                elif callable(target):
                    target()
                else:
                    if hasattr(target, "generate"):
                        target.generate()
                    else:
                        log.error(f"对象 {type(target).__name__} 没有 generate() 方法")
                        continue

                CliUtils.print("", end="\n")
            except Exception as e:
                log.error(f"执行菜单项 '{selected}' 时出错: {e}")
                CliUtils.print("", end="\n")
                continue
