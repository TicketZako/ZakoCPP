from internal.config import configer
from internal.util import CliUtils, log


class CliDebug:
    """
    debug 模式 配置
    """

    @staticmethod
    def generate():
        """
        配置窗口
        """
        CliUtils.print("", end="\n")
        CliUtils.print("调试模式配置", color="blue", size="large", style="underline")
        CliUtils.print("", end="\n")

        debug_result = CliUtils.inquire(
            type="Confirm",
            message="是否开启调试模式？",
            default=configer.setting.isDebug,
        )
        configer.setting.isDebug = bool(debug_result)

        log.info(f"调试模式已{'开启' if configer.setting.isDebug else '关闭'}")


class CliMaxConsecutiveRequest:
    """
    初始连续请求次数配置
    """

    @staticmethod
    def generate():
        """
        配置窗口
        """
        CliUtils.print("", end="\n")
        CliUtils.print(
            "初始连续请求次数配置", color="blue", size="large", style="underline"
        )
        CliUtils.print("", end="\n")

        while True:
            try:
                value = CliUtils.inquire(
                    type="Text",
                    message="请输入初始连续请求次数",
                    default=str(configer.setting.maxConsecutiveRequest),
                )

                if not value:
                    CliUtils.print("初始连续请求次数不能为空", color="red")
                    continue

                int_value = int(value)

                if int_value < 1:
                    CliUtils.print("初始连续请求次数必须大于0", color="red")
                    continue

                configer.setting.maxConsecutiveRequest = int_value
                CliUtils.print("", end="\n")
                CliUtils.print(
                    f"✅ 初始连续请求次数已设置为: {int_value}",
                    color="green",
                )
                log.info(f"初始连续请求次数已设置为: {int_value}")
                break

            except ValueError:
                CliUtils.print("请输入有效的数字", color="red")
                continue
            except Exception as e:
                log.error(f"配置初始连续请求次数失败: {e}")
                break


class CliRiskedInterval:
    """
    风控间隔配置
    """

    @staticmethod
    def generate():
        """
        配置窗口
        """
        CliUtils.print("", end="\n")
        CliUtils.print("风控间隔配置", color="blue", size="large", style="underline")
        CliUtils.print("", end="\n")

        while True:
            try:
                value = CliUtils.inquire(
                    type="Text",
                    message="请输入风控间隔（毫秒）",
                    default=str(configer.setting.riskedInterval),
                )

                if not value:
                    CliUtils.print("风控间隔不能为空", color="red")
                    continue

                int_value = int(value)

                if int_value < 0:
                    CliUtils.print("风控间隔不能为负数", color="red")
                    continue

                configer.setting.riskedInterval = int_value
                CliUtils.print("", end="\n")
                CliUtils.print(
                    f"✅ 风控间隔已设置为: {int_value} 毫秒 ({int_value / 1000:.1f} 秒)",
                    color="green",
                )
                log.info(f"风控间隔已设置为: {int_value} 毫秒")
                break

            except ValueError:
                CliUtils.print("请输入有效的数字", color="red")
                continue
            except Exception as e:
                log.error(f"配置风控间隔失败: {e}")
                break
