from typing import List, Optional, Tuple

from internal.client.api import ProductApi
from internal.config import configer
from internal.config.product import ProductMainData, ProductTypeData
from internal.error import ProductStatusCode
from internal.util import SystemUtils, log


class ProductService:
    """
    票务信息服务
    """

    @staticmethod
    def get_ticket(
        event_main_id: int,
    ) -> Tuple[int, Optional[ProductMainData], Optional[List[ProductTypeData]]]:
        """
        获取票务信息

        :param event_main_id: 活动 ID

        :return: 状态码, 活动, 票档信息列表
        """
        resp = ProductApi.query_product(event_main_id)

        if resp.data is None:
            return ProductStatusCode.Error, None, None

        product_main_data = ProductMainData(
            id=resp.data.ticketMain.eventMainId,
            name=resp.data.ticketMain.eventName,
        )

        product_type_data_list = [
            ProductTypeData(
                id=item.id,
                name=item.ticketName,
                square=item.square,
                price=item.ticketPrice,
                purchaseNum=item.purchaseNum,
                remainderNum=item.remainderNum,
                lockNum=item.lockNum,
                realnameAuth=item.realnameAuth,
                sellStartTime=item.sellStartTime,
                sellEndTime=item.sellEndTime,
            )
            for item in resp.data.ticketTypeList
        ]

        return resp.code, product_main_data, product_type_data_list

    @staticmethod
    def check_ticket() -> int:
        """
        是否有票

        :return: 状态码
        """
        event_main_id = configer.product.ticketMain.id
        ticket_type_id = configer.product.ticketType.id
        resp = ProductApi.query_product(event_main_id)

        if resp.data is None:
            return ProductStatusCode.Error

        for item in resp.data.ticketTypeList:
            if item.id != ticket_type_id:
                continue

            remainder_num = item.remainderNum
            lock_num = item.lockNum

            log.debug(f"余票数: {remainder_num} 已锁定数: {lock_num}")

            if remainder_num > 0:
                return ProductStatusCode.Success
            else:
                return ProductStatusCode.NoStock

        return ProductStatusCode.NoStock

    @staticmethod
    def check_inactive() -> int:
        """
        检查活动是否已结束

        :return: 状态码
        """
        event_main_id = configer.product.ticketMain.id
        ticket_type_id = configer.product.ticketType.id
        resp = ProductApi.query_product(event_main_id)

        if resp.data is None:
            return ProductStatusCode.Error

        for item in resp.data.ticketTypeList:
            if item.id != ticket_type_id:
                continue

            sell_end_time = item.sellEndTime
            current_time = SystemUtils.get_timestamp()

            if sell_end_time > current_time:
                return ProductStatusCode.Success
            else:
                return ProductStatusCode.Inactive

        return ProductStatusCode.Inactive
