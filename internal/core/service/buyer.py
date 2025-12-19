from typing import List, Tuple

from internal.client.api.buyer import BuyerApi
from internal.data.response import QueryBuyerData
from internal.error import BuyerStatusCode


class BuyerService:
    """
    购买人信息服务
    """

    @staticmethod
    def get_buyer() -> Tuple[int, List[QueryBuyerData]]:
        """
        获取购票人信息

        :return: 状态码, 购票人信息列表
        """
        response = BuyerApi.query_buyer()
        data = response.data

        if len(data) == 0:
            return BuyerStatusCode.MissingBuyer, []

        return BuyerStatusCode.Success, data
