from os import getcwd
from pathlib import Path
from socket import AF_INET, SOCK_DGRAM, socket
from time import sleep, time
from typing import Any, Optional

from httpx import Client


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
        退出程序（强制退出，不等待线程）

        :param code: 退出码
        """
        import os

        from internal.util.logger import log  # 防止循环导入

        if code != 0:
            log.error("出现异常，正在强制退出程序...")
        else:
            log.info("正在强制退出程序...")
        os._exit(code)


class IPUtils:
    """
    IP 工具类
    """

    @staticmethod
    def get_local_ip() -> str:
        """
        获取本机 IP 地址

        :return: IP 地址字符串
        """
        try:
            s = socket(AF_INET, SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception:
            return "127.0.0.1"

    @staticmethod
    def get_public_ip() -> Optional[str]:
        """
        获取公网 IP 地址（局域网对外出口IP）

        :return: 公网 IP 地址字符串
        """
        ip_services = [
            "https://api.ipify.org",
            "https://api.ip.sb/ip",
            "https://ifconfig.me/ip",
            "https://icanhazip.com",
        ]

        client = Client(timeout=5.0, verify=False)
        try:
            for service_url in ip_services:
                try:
                    response = client.get(service_url)
                    if response.status_code == 200:
                        ip = response.text.strip()
                        if ip and "." in ip:
                            return ip
                except Exception:
                    continue
        finally:
            client.close()

        return None
