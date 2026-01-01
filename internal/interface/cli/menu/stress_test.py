import signal
import sys
from random import randint
from time import sleep, time

from internal.util import CliUtils, TimeUtils, log


class CliStressTest:
    """
    压力测试
    """

    _testing = False
    _stats = {
        "total": 0,
        "success": 0,
        "failed": 0,
        "start_time": None,
    }

    @staticmethod
    def input_interval() -> float:
        """
        输入请求间隔（秒）
        """
        interval_str = CliUtils.inquire(
            type="Text",
            message="请输入请求间隔（秒，默认 0.1 秒，0 表示无间隔）",
            default="0.1",
        )

        try:
            interval = float(interval_str)
            if interval < 0:
                log.warning("请求间隔不能小于 0，使用默认值 0.1 秒")
                return 0.1
            return interval
        except ValueError:
            log.warning("请求间隔格式错误，使用默认值 0.1 秒")
            return 0.1

    @staticmethod
    def generate_random_ticket_type_id() -> int:
        """
        生成随机的四位数 ticket_type_id

        :return: 1000-9999 之间的随机整数
        """
        return randint(1000, 9999)

    @staticmethod
    def run_stress_test(interval: float):
        """
        运行压力测试

        :param interval: 请求间隔（秒）
        """
        CliStressTest._testing = True
        CliStressTest._stats = {
            "total": 0,
            "success": 0,
            "failed": 0,
            "start_time": time(),
        }

        def signal_handler(signum, frame):
            CliStressTest._testing = False
            CliUtils.print("", end="\n")
            CliUtils.print("正在停止压力测试...", color="yellow")
            sys.exit(0)

        signal.signal(signal.SIGINT, signal_handler)

        CliUtils.print("", end="\n")
        CliUtils.print("开始压力测试", color="green", bold=True)
        CliUtils.print(f"请求间隔: {interval} 秒", color="cyan")
        CliUtils.print("按 Ctrl+C 停止测试", color="yellow")
        CliUtils.print("", end="\n")

        while CliStressTest._testing:
            try:
                ticket_type_id = CliStressTest.generate_random_ticket_type_id()
                CliStressTest._stats["total"] += 1

                start_time = time()
                cpp_response = None
                elapsed = (time() - start_time) * 1000

                if cpp_response.code == 0:
                    CliStressTest._stats["success"] += 1
                    status_color = "green"
                    status_text = "✓"
                else:
                    CliStressTest._stats["failed"] += 1
                    status_color = "red"
                    status_text = "✗"

                elapsed_time = time() - CliStressTest._stats["start_time"]
                success_rate = (
                    CliStressTest._stats["success"]
                    / CliStressTest._stats["total"]
                    * 100
                    if CliStressTest._stats["total"] > 0
                    else 0
                )

                CliUtils.print(
                    f"[{TimeUtils.format_timestamp_time(int(time() * 1000))}] "
                    f"{status_text} Ticket ID: {ticket_type_id:4d} | "
                    f"响应: {cpp_response.msg[:30]} | "
                    f"耗时: {elapsed:.1f}ms | "
                    f"总计: {CliStressTest._stats['total']} | "
                    f"成功: {CliStressTest._stats['success']} | "
                    f"失败: {CliStressTest._stats['failed']} | "
                    f"成功率: {success_rate:.1f}% | "
                    f"运行时间: {int(elapsed_time)}s",
                    color=status_color,
                )

                if interval > 0:
                    sleep(interval)

            except KeyboardInterrupt:
                CliStressTest._testing = False
                CliUtils.print("", end="\n")
                CliUtils.print("压力测试已停止", color="yellow")
                break
            except Exception as e:
                CliStressTest._stats["failed"] += 1
                CliStressTest._stats["total"] += 1
                log.error(f"压力测试出错: {e}")
                CliUtils.print(
                    f"[{TimeUtils.format_timestamp_time(int(time() * 1000))}] "
                    f"✗ 错误: {str(e)[:50]}",
                    color="red",
                )

                if interval > 0:
                    sleep(interval)

        elapsed_time = time() - CliStressTest._stats["start_time"]
        success_rate = (
            CliStressTest._stats["success"] / CliStressTest._stats["total"] * 100
            if CliStressTest._stats["total"] > 0
            else 0
        )
        avg_time = (
            elapsed_time / CliStressTest._stats["total"]
            if CliStressTest._stats["total"] > 0
            else 0
        )

        CliUtils.print("", end="\n")
        CliUtils.print("=" * 60, color="cyan")
        CliUtils.print("压力测试统计", color="cyan", bold=True)
        CliUtils.print("=" * 60, color="cyan")
        CliUtils.print(f"总请求数: {CliStressTest._stats['total']}")
        CliUtils.print(f"成功: {CliStressTest._stats['success']}", color="green")
        CliUtils.print(f"失败: {CliStressTest._stats['failed']}", color="red")
        CliUtils.print(f"成功率: {success_rate:.2f}%")
        CliUtils.print(f"总运行时间: {int(elapsed_time)} 秒")
        CliUtils.print(f"平均请求时间: {avg_time:.3f} 秒")
        if elapsed_time > 0:
            qps = CliStressTest._stats["total"] / elapsed_time
            CliUtils.print(f"QPS: {qps:.2f}")
        CliUtils.print("=" * 60, color="cyan")
        CliUtils.print("", end="\n")

    @staticmethod
    def generate():
        """
        配置窗口
        """
        CliUtils.print("", end="\n")
        CliUtils.print("压力测试", color="cyan", size="large", style="underline")
        CliUtils.print("", end="\n")

        interval = CliStressTest.input_interval()

        CliStressTest.run_stress_test(interval)
