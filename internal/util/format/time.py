from datetime import datetime
from typing import Union


class TimeUtils:
    """
    时间格式化工具类
    """

    @staticmethod
    def format_timestamp(
        timestamp: Union[int, float],
        format_str: str = "%Y-%m-%d %H:%M:%S",
        is_milliseconds: bool = True,
    ) -> str:
        """
        将时间戳转换为可读的时间字符串

        :param timestamp: 时间戳（毫秒或秒）
        :param format_str: 时间格式字符串，默认为 "%Y-%m-%d %H:%M:%S"
        :param is_milliseconds: 是否为毫秒级时间戳，默认为 True
        :return: 格式化后的时间字符串
        """
        if timestamp is None:
            return ""

        # 如果是毫秒级时间戳，转换为秒
        if is_milliseconds:
            timestamp_seconds = timestamp / 1000.0
        else:
            timestamp_seconds = float(timestamp)

        # 转换为 datetime 对象
        dt = datetime.fromtimestamp(timestamp_seconds)

        # 格式化输出
        return dt.strftime(format_str)

    @staticmethod
    def format_timestamp_date(timestamp: Union[int, float]) -> str:
        """
        只显示日期部分

        :param timestamp: 毫秒级时间戳
        :return: 日期字符串，格式为 "YYYY-MM-DD"
        """
        return TimeUtils.format_timestamp(timestamp, format_str="%Y-%m-%d")

    @staticmethod
    def format_timestamp_datetime(timestamp: Union[int, float]) -> str:
        """
        显示日期和时间

        :param timestamp: 毫秒级时间戳
        :return: 日期时间字符串，格式为 "YYYY-MM-DD HH:MM:SS"
        """
        return TimeUtils.format_timestamp(timestamp, format_str="%Y-%m-%d %H:%M:%S")

    @staticmethod
    def format_timestamp_time(timestamp: Union[int, float]) -> str:
        """
        只显示时间部分

        :param timestamp: 毫秒级时间戳
        :return: 时间字符串，格式为 "HH:MM:SS"
        """
        return TimeUtils.format_timestamp(timestamp, format_str="%H:%M:%S")

    @staticmethod
    def format_timestamp_relative(timestamp: Union[int, float]) -> str:
        """
        转换为相对时间描述（如：刚刚、5分钟前、2小时前等）

        :param timestamp: 毫秒级时间戳
        :return: 相对时间描述
        """
        if timestamp is None:
            return ""

        from time import time

        # 获取当前时间戳（秒）
        current_timestamp = time()

        # 将毫秒时间戳转换为秒
        target_timestamp = timestamp / 1000.0

        # 计算时间差（秒）
        diff = current_timestamp - target_timestamp

        if diff < 0:
            return "未来时间"

        if diff < 60:
            return "刚刚"
        elif diff < 3600:
            minutes = int(diff / 60)
            return f"{minutes}分钟前"
        elif diff < 86400:
            hours = int(diff / 3600)
            return f"{hours}小时前"
        elif diff < 2592000:
            days = int(diff / 86400)
            return f"{days}天前"
        else:
            # 超过30天，显示具体日期
            return TimeUtils.format_timestamp_date(timestamp)
