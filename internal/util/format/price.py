from typing import Union


class PriceUtils:
    """
    价格格式化工具类
    """

    @staticmethod
    def format_price(
        price: Union[int, float], unit: str = "元", decimal_places: int = 2
    ) -> str:
        """
        将价格（分）转换为带小数点的元格式

        :param price: 价格（分），例如 7500 表示 75.00 元
        :param unit: 单位，默认为 "元"
        :param decimal_places: 小数位数，默认为 2
        :return: 格式化后的价格字符串，例如 "75.00元"
        """
        if price is None:
            return f"0.{'0' * decimal_places}{unit}"

        # 将分转换为元
        yuan = price / 100.0

        # 格式化小数位数
        formatted = f"{yuan:.{decimal_places}f}"

        return f"{formatted}{unit}"
