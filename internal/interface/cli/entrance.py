from internal.interface.cli.menu import (
    CliBuyer,
    CliDebug,
    CliInit,
    CliLaunch,
    CliLogin,
    CliMaxConsecutiveRequest,
    CliNotification,
    CliProduct,
    CliRefreshInterval,
    CliRiskedInterval,
    CliStressTest,
    CliTicketMonitor,
)
from internal.util import CliUtils
from internal.version import __version__


class CliEntrance:
    """
    交互界面入口
    """

    @staticmethod
    def enter():
        """
        进入界面
        """
        ascii_lines = [
            "",
            "                                                 ",
            " mmmmmm        #               mmm  mmmmm  mmmmm ",
            '     #"  mmm   #   m   mmm   m"   " #   "# #   "#',
            '   m#   "   #  # m"   #" "#  #      #mmm#" #mmm#"',
            '  m"    m"""#  #"#    #   #  #      #      #     ',
            ' ##mmmm "mm"#  #  "m  "#m#"   "mmm" #      #     ',
            "                                                 ",
            "",
        ]
        for line in ascii_lines:
            print(line)
        CliUtils.print(
            "Copyright (c) 2025 TicketZako <https://github.com/TicketZako>",
            color="green",
        )
        CliUtils.print("", end="\n")
        CliUtils.print(
            f"Version: {__version__}",
            color="cyan",
        )
        CliUtils.print("", end="\n")
        CliUtils.print(
            "This is free software, licensed under the Apache License 2.0.",
            color="yellow",
        )
        CliUtils.print("", end="\n")

        CliInit.init()

        CliUtils.menu(
            title="主菜单",
            items=[
                {
                    "name": "启动抢票",
                    "target": CliLaunch,
                },
                {
                    "name": "购票信息",
                    "target": CliBuyer,
                },
                {
                    "name": "票务选购",
                    "target": CliProduct,
                },
                {
                    "name": "票务监控",
                    "target": CliTicketMonitor,
                },
                {
                    "name": "重新登录",
                    "target": CliLogin,
                },
                {
                    "name": "通知配置",
                    "target": CliNotification,
                },
                {
                    "name": "系统设置",
                    "target": {
                        "title": "系统设置",
                        "items": [
                            {
                                "name": "调试模式配置",
                                "target": CliDebug,
                            },
                            {
                                "name": "初始连续请求次数配置",
                                "target": CliMaxConsecutiveRequest,
                            },
                            {
                                "name": "风控间隔配置",
                                "target": CliRiskedInterval,
                            },
                            {
                                "name": "刷新余票间隔配置",
                                "target": CliRefreshInterval,
                            },
                        ],
                    },
                },
                {
                    "name": "压力测试",
                    "target": CliStressTest,
                },
            ],
            is_top_level=True,
        )
