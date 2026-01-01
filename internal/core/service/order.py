from typing import Tuple

from internal.client.api import OrderApi
from internal.config import configer
from internal.error import OrderStatusCode
from internal.util.parser import ParserUtils


class OrderService:
    """
    订单服务
    """

    @staticmethod
    def create_order() -> Tuple[int, str, str]:
        """
        创建订单

        :return: 状态码，订单编号，订单 URL
        """
        resp = OrderApi().create_order(
            method=configer.product.ticketMethod,
            ticket_type_id=configer.product.ticketType.id,
            ticket_count=configer.buyer.count,
            purchaser_ids=",".join([str(b.id) for b in configer.buyer.buyer]),
        )

        if resp.code == OrderStatusCode.Success and resp.data:
            order_id = resp.data.outTradeNo
            order_info = ParserUtils.unmarshal_query(resp.data.orderInfo)
            order_url = order_info["return_url"]

        else:
            order_id = ""
            order_url = ""

        return resp.code, order_id, order_url
