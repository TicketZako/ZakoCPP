import signal
import sys
from time import sleep

from internal.core.service import ProductService
from internal.error import ProductStatusCode
from internal.util import CliUtils, PriceUtils, SystemUtils, TimeUtils, log
from internal.util.logger import log_settings


class CliTicketMonitor:
    """
    票务监控
    """

    _monitoring = False
    _event_id = None

    @staticmethod
    def input_event_id() -> int | None:
        """
        输入活动 ID
        """
        event_main_id = CliUtils.inquire(
            type="Text",
            message="请输入活动 ID",
            default="5476",
        )

        if not event_main_id:
            log.warning("活动 ID 不能为空")
            return None

        try:
            return int(event_main_id)
        except ValueError:
            log.error("活动 ID 格式错误，请输入数字")
            return None

    @staticmethod
    def input_refresh_interval() -> int:
        """
        输入刷新间隔（秒）
        """
        interval_str = CliUtils.inquire(
            type="Text",
            message="请输入刷新间隔（秒，0表示立即刷新，默认 5 秒）",
            default="5",
        )

        try:
            interval = int(interval_str)
            if interval < 0:
                log.warning("刷新间隔不能小于 0 秒，使用默认值 5 秒")
                return 5
            return interval
        except ValueError:
            log.warning("刷新间隔格式错误，使用默认值 5 秒")
            return 5

    @staticmethod
    def input_only_on_change() -> bool:
        """
        输入是否只在余数变化时输出
        """
        return bool(
            CliUtils.inquire(
                type="Confirm",
                message="是否只在票务余数发生变化时输出？",
                default=False,
            )
        )

    @staticmethod
    def display_ticket_info(ticket_main, ticket_types):
        """
        显示票务信息
        """
        CliUtils.print("", end="\n")
        CliUtils.print("=" * 60, color="cyan")
        CliUtils.print(f"活动名称: {ticket_main.name}", color="cyan", bold=True)
        CliUtils.print(f"活动 ID: {ticket_main.id}", color="cyan")
        CliUtils.print("=" * 60, color="cyan")
        CliUtils.print("", end="\n")

        if not ticket_types:
            CliUtils.print("该活动没有可用票务", color="yellow")
            return

        CliUtils.print("票档列表:", color="yellow", bold=True)
        CliUtils.print("", end="\n")

        for idx, ticket in enumerate(ticket_types, 1):
            CliUtils.print(f"【票档 {idx}】", color="green", bold=True)
            CliUtils.print(f"  票档 ID: {ticket.id}")
            CliUtils.print(f"  票档名称: {ticket.name}")
            if ticket.square:
                CliUtils.print(f"  场次名称: {ticket.square}")
            CliUtils.print(f"  票务价格: {PriceUtils.format_price(ticket.price)}")
            CliUtils.print(f"  可购买数量: {ticket.purchaseNum}张")

            if ticket.remainderNum > 0:
                CliUtils.print(
                    f"  剩余数量: {ticket.remainderNum}张",
                    color="green",
                )
            else:
                CliUtils.print(
                    f"  剩余数量: {ticket.remainderNum}张",
                    color="red",
                )

            CliUtils.print(f"  已锁定数量: {ticket.lockNum}张")

            current_time = SystemUtils.get_timestamp()
            if ticket.sellStartTime > current_time:
                time_left = (ticket.sellStartTime - current_time) / 1000
                CliUtils.print(
                    f"  开票时间: 未开票，还有 {int(time_left)} 秒",
                    color="yellow",
                )
            else:
                CliUtils.print(
                    "  开票时间: 已开票",
                    color="green",
                )

            CliUtils.print(f"  实名制购票: {'是' if ticket.realnameAuth else '否'}")

            if ticket.sellEndTime < current_time:
                CliUtils.print("  状态: 已结束", color="red", bold=True)
            elif ticket.remainderNum > 0:
                CliUtils.print("  状态: 有票", color="green", bold=True)
            else:
                CliUtils.print("  状态: 无票", color="red", bold=True)

            CliUtils.print("", end="\n")

    @staticmethod
    def monitor_ticket(
        event_id: int, refresh_interval: int, only_on_change: bool = False
    ):
        """
        监控票务状态

        :param event_id: 活动 ID
        :param refresh_interval: 刷新间隔（秒）
        :param only_on_change: 是否只在余数变化时输出
        """
        CliTicketMonitor._monitoring = True
        CliTicketMonitor._event_id = event_id

        def signal_handler(signum, frame):
            CliTicketMonitor._monitoring = False
            CliUtils.print("", end="\n")
            CliUtils.print("正在停止监控...", color="yellow")
            sys.exit(0)

        signal.signal(signal.SIGINT, signal_handler)

        original_log_level = log_settings.LOG_LEVEL
        log_settings.LOG_LEVEL = "CRITICAL"

        def restore_log_level():
            """恢复原始日志级别"""
            log_settings.LOG_LEVEL = original_log_level

        CliUtils.print("", end="\n")
        CliUtils.print("开始监控票务状态", color="green", bold=True)
        CliUtils.print(f"刷新间隔: {refresh_interval} 秒", color="cyan")
        if only_on_change:
            CliUtils.print("输出模式: 仅在余数变化时输出", color="cyan")
        CliUtils.print("按 Ctrl+C 退出监控", color="yellow")
        CliUtils.print("", end="\n")

        first_run = True
        previous_remainders = {}

        while CliTicketMonitor._monitoring:
            try:
                resp = ProductService.get_ticket(event_id)
                status_code, ticket_main, ticket_types = resp

                if status_code != ProductStatusCode.Success:
                    if first_run:
                        log.error("获取票务信息失败")
                        CliUtils.print("获取票务信息失败", color="red")
                        break
                    else:
                        log.warning("获取票务信息失败，继续重试...")
                        if not only_on_change:
                            CliUtils.print(
                                f"[{TimeUtils.format_timestamp_time(SystemUtils.get_timestamp())}] 获取票务信息失败，继续重试...",
                                color="yellow",
                            )
                else:
                    has_change = False
                    if only_on_change and not first_run:
                        current_remainders = {
                            ticket.id: ticket.remainderNum for ticket in ticket_types
                        }
                        for ticket_id, current_remainder in current_remainders.items():
                            previous_remainder = previous_remainders.get(ticket_id)
                            if (
                                previous_remainder is not None
                                and previous_remainder != current_remainder
                            ):
                                has_change = True
                                break
                        if not has_change and len(current_remainders) != len(
                            previous_remainders
                        ):
                            has_change = True
                    else:
                        has_change = True

                    if has_change:
                        if not first_run:
                            print("\033[2J\033[H", end="")
                            CliUtils.print("", end="\n")
                            CliUtils.print(
                                f"[{TimeUtils.format_timestamp_time(SystemUtils.get_timestamp())}] 刷新中...",
                                color="cyan",
                            )

                        CliTicketMonitor.display_ticket_info(ticket_main, ticket_types)

                        previous_remainders = {
                            ticket.id: ticket.remainderNum for ticket in ticket_types
                        }
                    elif only_on_change and not first_run:
                        CliUtils.print(
                            f"[{TimeUtils.format_timestamp_time(SystemUtils.get_timestamp())}] 余数未变化，跳过输出...",
                            style="dim",
                        )

                    if first_run:
                        first_run = False

                if CliTicketMonitor._monitoring:
                    if refresh_interval > 0:
                        CliUtils.print(
                            f"下次刷新: {refresh_interval} 秒后 (按 Ctrl+C 退出)",
                            style="dim",
                            size="small",
                        )
                        CliUtils.print("", end="\n")

                        for remaining in range(refresh_interval, 0, -1):
                            if not CliTicketMonitor._monitoring:
                                break
                            sleep(1)
                    else:
                        CliUtils.print(
                            "立即刷新中... (按 Ctrl+C 退出)",
                            style="dim",
                            size="small",
                        )
                        CliUtils.print("", end="\n")

            except KeyboardInterrupt:
                CliTicketMonitor._monitoring = False
                restore_log_level()
                CliUtils.print("", end="\n")
                CliUtils.print("监控已停止", color="yellow")
                break
            except Exception as e:
                if first_run:
                    CliUtils.print(f"监控出错: {e}", color="red")
                    restore_log_level()
                    break
                else:
                    if not only_on_change:
                        CliUtils.print(
                            f"[{TimeUtils.format_timestamp_time(SystemUtils.get_timestamp())}] 监控出错: {e}，继续重试...",
                            color="yellow",
                        )
                    sleep(refresh_interval)

        restore_log_level()

    @staticmethod
    def generate():
        """
        配置窗口
        """
        CliUtils.print("", end="\n")
        CliUtils.print("票务监控", color="cyan", size="large", style="underline")
        CliUtils.print("", end="\n")

        # 输入活动 ID
        event_id = CliTicketMonitor.input_event_id()
        if event_id is None:
            return

        # 输入刷新间隔
        refresh_interval = CliTicketMonitor.input_refresh_interval()

        # 输入是否只在余数变化时输出
        only_on_change = CliTicketMonitor.input_only_on_change()

        # 开始监控
        CliTicketMonitor.monitor_ticket(event_id, refresh_interval, only_on_change)
