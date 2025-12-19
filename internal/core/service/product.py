from typing import List, Tuple

from internal.client.api.product import ProductApi
from internal.config import configer
from internal.data.response import QueryProductTypeData, QueryPruductMainData
from internal.error import ProductStatusCode
from internal.util import log


class ProductService:
    """
    票务信息服务
    """

    @staticmethod
    def get_ticket(
        event_main_id: int,
    ) -> Tuple[int, QueryPruductMainData, List[QueryProductTypeData]]:
        """
        获取票务数据

        :return: 票务数据
        """
        resp = ProductApi.query_product(event_main_id)

        return resp.code, resp.data.ticketMain, resp.data.ticketTypeList

    @staticmethod
    def check_ticket() -> int:
        """
        是否有票

        :return: 状态码
        """
        event_main_id = configer.product.ticketMain.id
        ticket_type_id = configer.product.ticketType.id
        data = ProductApi.query_product(event_main_id).data.ticketTypeList

        for item in data:
            if item.id == ticket_type_id:
                remainder_num = item.remainderNum
                lock_num = item.lockNum

                log.debug(f"余票数: {remainder_num} 已锁定数: {lock_num}")

                if remainder_num > 0:
                    return ProductStatusCode.Success
                else:
                    return ProductStatusCode.NoStock

        return ProductStatusCode.NoStock
