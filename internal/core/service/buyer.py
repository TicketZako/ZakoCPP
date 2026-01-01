from typing import List, Tuple

from internal.client.api import BuyerApi
from internal.config.buyer import BuyerData
from internal.error import BuyerStatusCode


class BuyerService:
    """
    购买人信息服务
    """

    @staticmethod
    def get_buyer() -> Tuple[int, List[BuyerData]]:
        """
        获取购票人信息

        :return: 状态码, 购票人信息列表
        """
        resp = BuyerApi.query_buyer()

        if resp.data is None:
            return BuyerStatusCode.Error, []

        buyer_data_list = resp.data

        if len(buyer_data_list) == 0:
            return BuyerStatusCode.MissingBuyer, []

        buyer_data_list = [
            BuyerData(
                id=item.id,
                realname=item.realname,
                idcard=item.idcard,
                mobile=item.mobile,
                validType=item.validType,
            )
            for item in buyer_data_list
        ]

        return BuyerStatusCode.Success, buyer_data_list
