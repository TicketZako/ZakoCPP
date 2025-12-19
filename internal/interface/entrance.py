from internal.config import configer
from internal.core.service.user import UserService
from internal.error import LoginStatusCode
from internal.interface.cli.buyer import CliBuyer
from internal.interface.cli.launch import CliLaunch
from internal.interface.cli.notification import CliNotification
from internal.interface.cli.product import CliProduct
from internal.interface.cli.setting import (
    CliDebug,
    CliMaxConsecutiveRequest,
    CliRiskedInterval,
)
from internal.interface.cli.user import CliLogin
from internal.util import CliUtils, log


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
            "This is free software, licensed under the GNU General Public License v3.0.",
            color="yellow",
        )
        CliUtils.print("", end="\n")

        log.info("账户初始化中...")
        if not configer.account.account or not configer.account.password:
            log.warn("未登入 CPP，请先登入！")
            CliLogin.generate()
        else:
            if UserService.login() != LoginStatusCode.Success:
                log.warn("账户失效，重新登入！")
                CliLogin.generate()
        log.info("账户初始化完成")

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
                    "name": "重新登入",
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
                        ],
                    },
                },
            ],
            is_top_level=True,
        )
