from os import getcwd
from pathlib import Path
from sys import exit
from time import sleep, time
from typing import Any, Optional


class SystemUtils:
    """
    系统工具类
    """

    @staticmethod
    def get_data_path(path: Optional[Any] = None) -> Path:
        """
        数据文件目录

        :return: 数据文件目录
        """
        if path:
            return Path(path)
        else:
            return Path(getcwd())

    @staticmethod
    def get_config_path(path: Optional[Any] = None) -> Path:
        """
        获取配置文件目录

        :return: 配置文件目录
        """
        return SystemUtils.get_data_path(path) / "config"

    @staticmethod
    def get_machine_id() -> str:
        """
        获取机器 ID

        :return: 机器 ID
        """

    @staticmethod
    def get_timestamp() -> int:
        """
        获取毫米级时间戳

        :return: 时间戳
        """
        return int(time() * 1000)

    @staticmethod
    def sleep(t: int | float) -> None:
        """
        毫秒级休眠工具

        :param t: 休眠时间（毫秒）
        """
        sleep(t / 1000.0)

    @staticmethod
    def exit(code: int = 0) -> None:
        """
        退出程序

        :param code: 退出码
        """
        from internal.util.logger import log  # 防止循环导入

        if code != 0:
            log.error("出现异常，正在退出程序...")
        else:
            log.info("正在退出程序...")
        exit(code)
